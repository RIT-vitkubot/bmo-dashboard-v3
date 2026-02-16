import sqlite3
import os
import datetime
import functools

# Handle different DB paths depending on where it's run from
DB_PATH = os.path.join(os.path.dirname(__file__), 'bmo_dashboard.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def log_token_usage(model_name, prompt_tokens, completion_tokens, success, error_message=None):
    """Logs token usage to the database."""
    try:
        conn = get_db_connection()
        total_tokens = prompt_tokens + completion_tokens
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Ensure table exists (just in case)
        conn.execute('''
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
        
        conn.execute('''
            INSERT INTO token_usage (
                timestamp, model_name, prompt_tokens, completion_tokens, 
                total_tokens, api_call_count, success, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp, model_name, prompt_tokens, completion_tokens, 
            total_tokens, 1, success, error_message
        ))
        conn.commit()
        conn.close()
        print(f"Logged token usage: {total_tokens} tokens for {model_name}")
    except Exception as e:
        print(f"Failed to log token usage: {e}")

def monitor_gemini_usage(model_name_arg="gemini-1.5-flash"):
    """
    Decorator to monitor Gemini API usage.
    Expects the decorated function to return the full API response (dict).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Determine model name from args or kwargs if possible, otherwise use default
            model = kwargs.get('model_name', model_name_arg)
            
            try:
                result = func(*args, **kwargs)
                
                # If result is a dict, attempt to extract usage
                if isinstance(result, dict):
                    usage = result.get('usageMetadata', {})
                    prompt_tokens = usage.get('promptTokenCount', 0)
                    completion_tokens = usage.get('candidatesTokenCount', 0)
                    
                    log_token_usage(model, prompt_tokens, completion_tokens, True)
                
                return result
            except Exception as e:
                # Log failure
                error_msg = str(e)
                log_token_usage(model, 0, 0, False, error_msg)
                raise e # Re-raise exception
        return wrapper
    return decorator
