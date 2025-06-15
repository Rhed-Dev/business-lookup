import json
import os
import threading
from typing import List, Dict

CHAT_HISTORY_FILE = "data/chat_history.json"
CHAT_HISTORY_LOCK = threading.Lock()

# Initialize chat_history.json if it does not exist
if not os.path.exists(CHAT_HISTORY_FILE):
    os.makedirs(os.path.dirname(CHAT_HISTORY_FILE), exist_ok=True)
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

def save_message(session_id: str, message: Dict):
    """
    Save a message to the chat history for a given session.
    """
    with CHAT_HISTORY_LOCK:
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = {}
        if session_id not in history:
            history[session_id] = []
        history[session_id].append(message)
        with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

def get_history(session_id: str) -> List[Dict]:
    """
    Retrieve the chat history for a given session.
    """
    with CHAT_HISTORY_LOCK:
        if not os.path.exists(CHAT_HISTORY_FILE):
            return []
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
        return history.get(session_id, [])
