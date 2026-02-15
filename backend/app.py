from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import psutil
import os

app = Flask(__name__, static_folder='../frontend/dist')
CORS(app)

TASKS_FILE = os.path.join(os.path.dirname(__file__), '..', 'tasks.json')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    })

@app.route('/api/bmo-says', methods=['GET'])
def bmo_says():
    # Placeholder for BMO's proactive advice
    return jsonify({
        "message": "Vítku, you've been working on the Dashboard for a while. Don't forget to hydrate! 🕹️💧"
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
