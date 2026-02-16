import requests
import os
import time
from token_monitor import monitor_gemini_usage

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

@monitor_gemini_usage()
def _raw_gemini_call(prompt, model_name="gemini-1.5-flash"):
    """
    Internal function to make the raw API call.
    Returns the JSON response (dict).
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    url = GEMINI_API_URL.format(model_name=model_name, api_key=GEMINI_API_KEY)
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def call_gemini(prompt, model_name="gemini-1.5-flash"):
    """
    Public function to call Gemini and get text response.
    """
    try:
        # Call the decorated function
        result = _raw_gemini_call(prompt, model_name=model_name)
        
        # Extract response text
        try:
            candidates = result.get('candidates', [])
            if candidates:
                return candidates[0]['content']['parts'][0]['text']
            else:
                return "No response generated."
        except (KeyError, IndexError):
            return "Error parsing response structure."
            
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error calling Gemini API: {e}"

def call_ollama(prompt, model_name="llama3"):
    """
    Calls Ollama API (mock implementation).
    Does NOT log token usage to the token_usage table.
    """
    print(f"Calling Ollama with model {model_name}...")
    # Simulate response
    return f"Response from Ollama ({model_name}): {prompt}"
