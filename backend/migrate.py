import sqlite3
import json
import os
import datetime

DB_PATH = '/home/god/.openclaw/workspace/dashboard-v3/backend/bmo_dashboard.db'
TASKS_JSON = '/home/god/.openclaw/workspace/dashboard-v3/tasks.json'

def migrate():
    print("Starting migration...")
    
    # Connect to (or create) the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT CHECK(status IN ('Pending', 'Active', 'Completed')) NOT NULL DEFAULT 'Pending',
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Map old statuses to new ones if necessary
    status_map = {
        "ToDo": "Pending",
        "In Progress": "Active",
        "Done": "Completed"
    }

    # Load tasks from JSON
    if os.path.exists(TASKS_JSON):
        with open(TASKS_JSON, 'r') as f:
            tasks = json.load(f)
            
        for task in tasks:
            # Check if task already exists by title to avoid duplicates during multiple runs
            cursor.execute("SELECT id FROM activities WHERE title = ?", (task['title'],))
            if cursor.fetchone():
                print(f"Skipping duplicate: {task['title']}")
                continue
                
            status = status_map.get(task['status'], 'Pending')
            
            cursor.execute('''
            INSERT INTO activities (title, description, status, last_updated)
            VALUES (?, ?, ?, ?)
            ''', (task['title'], task['description'], status, task['last_updated']))
            print(f"Migrated: {task['title']}")
    else:
        print("tasks.json not found, nothing to migrate.")

    conn.commit()
    conn.close()
    print("Migration finished.")

if __name__ == "__main__":
    migrate()
