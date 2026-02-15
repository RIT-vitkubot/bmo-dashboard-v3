from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import psutil
import os
import sqlite3
import datetime
import time

app = Flask(__name__, static_folder='../frontend/dist')
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'bmo_dashboard.db')

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

@app.route('/api/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM activities WHERE id = ?', (id,))
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
