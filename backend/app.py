import json
import psutil
import os
import sqlite3
import datetime
import time
import subprocess
import re
import random
import caldav
from caldav.elements import dav
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import gemini_service

app = Flask(__name__, static_folder='../frontend/dist')
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'bmo_dashboard.db')
AUTH_PATH = os.path.join(os.path.dirname(__file__), 'calendar_auth.json')
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT CHECK(status IN ('Pending', 'Active', 'Completed')) NOT NULL DEFAULT 'Pending',
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS token_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        model_name TEXT NOT NULL,
        prompt_tokens INTEGER,
        completion_tokens INTEGER,
        total_tokens INTEGER,
        api_call_count INTEGER DEFAULT 1,
        success BOOLEAN,
        error_message TEXT
    )
    ''')
    conn.commit()
    conn.close()

def check_git_automation():
    """Checks git log for #complete <id> and updates database."""
    try:
        # Get last 10 commits
        output = subprocess.check_output(
            ['git', 'log', '-n', '10', '--pretty=format:%s'],
            cwd=REPO_PATH,
            stderr=subprocess.STDOUT
        ).decode('utf-8')
        
        matches = re.findall(r'#complete\s+(\d+)', output, re.IGNORECASE)
        if matches:
            conn = get_db_connection()
            for activity_id in matches:
                conn.execute('''
                    UPDATE activities 
                    SET status = "Completed", last_updated = ?
                    WHERE id = ? AND status != "Completed"
                ''', (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), activity_id))
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Git automation error: {e}")

init_db()
check_git_automation()

@app.route('/api/tasks', methods=['GET'])
@app.route('/api/activities', methods=['GET'])
def get_activities():
    check_git_automation()
    try:
        conn = get_db_connection()
        activities = conn.execute('SELECT * FROM activities').fetchall()
        conn.close()
        return jsonify([dict(row) for row in activities])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/activities', methods=['POST'])
def add_activity():
    try:
        data = request.json
        title = data.get('title')
        description = data.get('description', '')
        status = data.get('status', 'Pending')

        if not title:
            return jsonify({"status": "error", "message": "Title is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO activities (title, description, status, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (title, description, status, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        
        return jsonify({"status": "success", "id": new_id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/activities/<int:id>/status', methods=['PATCH'])
def update_activity_status(id):
    try:
        data = request.json
        status = data.get('status')
        if status not in ('Pending', 'Active', 'Completed'):
            return jsonify({"status": "error", "message": "Invalid status"}), 400

        conn = get_db_connection()
        conn.execute('''
            UPDATE activities 
            SET status = ?, last_updated = ?
            WHERE id = ?
        ''', (status, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    # Uptime
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_string = str(datetime.timedelta(seconds=int(uptime_seconds)))

    # Network
    net_io = psutil.net_io_counters(pernic=True)
    # Check for common VPN/Tunnel interfaces
    vpn_ifaces = ['tun0', 'wg0', 'wireguard']
    vpn_stats = {}
    for iface in vpn_ifaces:
        if iface in net_io:
            vpn_stats[iface] = {
                "bytes_sent": net_io[iface].bytes_sent,
                "bytes_recv": net_io[iface].bytes_recv
            }

    return jsonify({
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "uptime": uptime_string,
        "vpn": vpn_stats
    })

@app.route('/api/bmo-says', methods=['GET'])
def bmo_says():
    # Logic based on uptime and active tasks
    uptime_hours = (time.time() - psutil.boot_time()) / 3600
    
    conn = get_db_connection()
    active_count = conn.execute('SELECT COUNT(*) FROM activities WHERE status = "Active"').fetchone()[0]
    conn.close()

    # Try Gemini if key exists
    if os.environ.get('GEMINI_API_KEY'):
        prompt = f"You are BMO from Adventure Time, a helpful robot assistant. The system uptime is {int(uptime_hours)} hours. There are {active_count} active tasks. Generate a very short (max 1 sentence), cute, encouraging message for your user 'Vítku'."
        try:
            message = gemini_service.call_gemini(prompt)
            return jsonify({"message": message})
        except Exception as e:
            print(f"Gemini fallback: {e}")

    messages = [
        "Vítku, system is running smoothly. Phase 3: Intelligence is here! 🤖✨",
        "BMO is observing your progress. Keep going!",
        "Internal circuits are optimal. No errors found.",
        "Remember to stay hydrated while coding! 🥤"
    ]

    if active_count > 3:
        messages.append(f"Whoa, {active_count} active tasks? You're a machine, Vítku!")
    elif active_count == 0:
        messages.append("All tasks cleared! Time for a video game? 🎮")

    if uptime_hours > 24:
        messages.append(f"Server has been running for {int(uptime_hours)} hours. Rock solid! 💪")

    return jsonify({
        "message": random.choice(messages)
    })

@app.route('/api/calendar', methods=['GET'])
def get_calendar():
    try:
        with open(AUTH_PATH, 'r') as f:
            auth = json.load(f)
        
        username = auth.get('email')
        password = auth.get('password')
        url = "https://caldav.icloud.com"

        client = caldav.DAVClient(url, username=username, password=password)
        principal = client.principal()
        calendars = principal.calendars()
        
        if not calendars:
            return jsonify([])

        now = datetime.datetime.now()
        end = now + datetime.timedelta(days=7)
        
        all_events = []
        for calendar in calendars:
            cal_name = calendar.name
            events = calendar.date_search(start=now, end=end, expand=True)
            for event in events:
                vobj = event.vobject_instance.vevent
                
                summary = vobj.summary.value if hasattr(vobj, 'summary') else 'No Title'
                
                # Handle start time
                start_dt = vobj.dtstart.value
                is_all_day = not isinstance(start_dt, datetime.datetime)
                
                if isinstance(start_dt, datetime.datetime):
                    # Localize if it's naive (iCloud usually sends TZ aware, but just in case)
                    start_time = start_dt.strftime('%H:%M')
                    sort_key = start_dt.timestamp()
                else:
                    # Date object (all day)
                    start_time = "Celý den"
                    # Sort all day events at the beginning of the day
                    sort_key = datetime.datetime.combine(start_dt, datetime.time.min).timestamp()

                all_events.append({
                    "title": summary,
                    "time": start_time,
                    "allDay": is_all_day,
                    "calendar": cal_name,
                    "sort_key": sort_key
                })

        # Sort by time and take top 10 (Frontend will slice to 3-4)
        all_events.sort(key=lambda x: x['sort_key'])
        
        # Remove duplicates
        seen = set()
        unique_events = []
        for e in all_events:
            identifier = f"{e['title']}-{e['time']}"
            if identifier not in seen:
                seen.add(identifier)
                unique_events.append(e)

        return jsonify(unique_events[:10])

    except Exception as e:
        print(f"Calendar error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    try:
        # Get cron jobs from OpenClaw
        output = subprocess.check_output(
            ['openclaw', 'cron', 'list', '--json'],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
        
        data = json.loads(output)
        jobs = data.get('jobs', [])
        
        schedule = []
        now_ms = time.time() * 1000
        
        for job in jobs:
            next_run_ms = job.get('state', {}).get('nextRunAtMs')
            if not next_run_ms:
                continue
            
            # Calculate relative time or format absolute time
            diff_ms = next_run_ms - now_ms
            
            if diff_ms < 0:
                time_str = "soon"
            elif diff_ms < 3600000: # < 1h
                time_str = f"in {int(diff_ms / 60000)}m"
            elif diff_ms < 86400000: # < 24h
                time_str = f"in {int(diff_ms / 3600000)}h"
            else:
                dt = datetime.datetime.fromtimestamp(next_run_ms / 1000)
                time_str = dt.strftime('%a %H:%M')

            schedule.append({
                "name": job.get('name', 'Unnamed Job'),
                "time": time_str,
                "status": "Enabled" if job.get('enabled') else "Disabled",
                "next_run_ms": next_run_ms
            })
        
        # Sort by next run
        schedule.sort(key=lambda x: x['next_run_ms'])
        
        return jsonify(schedule)
    except Exception as e:
        print(f"Schedule error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/token-usage/daily', methods=['GET'])
def get_token_usage_daily():
    try:
        conn = get_db_connection()
        # Last 7 days
        query = '''
            SELECT date(timestamp) as date, SUM(total_tokens) as tokens
            FROM token_usage
            WHERE timestamp >= date('now', '-6 days')
            GROUP BY date(timestamp)
            ORDER BY date(timestamp)
        '''
        rows = conn.execute(query).fetchall()
        conn.close()
        
        # Fill in missing dates
        data = {row['date']: row['tokens'] for row in rows}
        result = []
        for i in range(6, -1, -1):
            d = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            result.append({
                "date": d,
                "tokens": data.get(d, 0)
            })
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/token-usage/monthly', methods=['GET'])
def get_token_usage_monthly():
    try:
        conn = get_db_connection()
        # Current month
        query = '''
            SELECT SUM(total_tokens) as tokens
            FROM token_usage
            WHERE strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
        '''
        row = conn.execute(query).fetchone()
        conn.close()
        return jsonify({"month": datetime.datetime.now().strftime('%Y-%m'), "tokens": row['tokens'] or 0})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/token-usage/models', methods=['GET'])
def get_token_usage_models():
    try:
        conn = get_db_connection()
        query = '''
            SELECT model_name, SUM(total_tokens) as tokens
            FROM token_usage
            GROUP BY model_name
            ORDER BY tokens DESC
        '''
        rows = conn.execute(query).fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/token-usage/status', methods=['GET'])
def get_token_usage_status():
    try:
        limit = 1000000 # Configurable limit
        conn = get_db_connection()
        query = '''
            SELECT SUM(total_tokens) as tokens
            FROM token_usage
            WHERE strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
        '''
        row = conn.execute(query).fetchone()
        conn.close()
        
        used = row['tokens'] or 0
        status = "OK"
        if used > limit:
            status = "Limit Exceeded"
        elif used > limit * 0.8:
            status = "Approaching Limit"
            
        return jsonify({
            "status": status,
            "used": used,
            "limit": limit,
            "percentage": round((used / limit) * 100, 2)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Serve Frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
