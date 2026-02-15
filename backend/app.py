from flask import Flask, jsonify
from flask_cors import CORS
import json
import psutil
import os

app = Flask(__name__)
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
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    })

@app.route('/api/bmo-says', methods=['GET'])
def bmo_says():
    # Placeholder for BMO's proactive advice
    return jsonify({
        "message": "Vítku, you've been working on the Dashboard for a while. Don't forget to hydrate! 🕹️💧"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
