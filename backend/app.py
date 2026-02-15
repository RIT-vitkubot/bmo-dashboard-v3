from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import psutil
import os
import sqlite3
import datetime
import time
import caldav
from caldav.elements import dav

app = Flask(__name__, static_folder='../frontend/dist')
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'bmo_dashboard.db')
AUTH_PATH = os.path.join(os.path.dirname(__file__), 'calendar_auth.json')

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
    conn.commit()
    conn.close()

init_db()

@app.route('/api/tasks', methods=['GET'])
@app.route('/api/activities', methods=['GET'])
def get_activities():
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
    return jsonify({
        "message": "Vítku, system is running smoothly. Phase 2: The Heart is now pulsing! 🤖💓"
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
                    "sort_key": sort_key
                })

        # Sort by time and take top 10 (Frontend will slice to 3-4)
        all_events.sort(key=lambda x: x['sort_key'])
        
        # Remove duplicates (sometimes multiple calendars or weird iCloud things)
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
