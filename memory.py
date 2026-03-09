"""
Conversation memory — persists chat history to JSON files.
Each session gets a unique file, and past sessions can be listed/resumed.
"""

import json
import os
from datetime import datetime

MEMORY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conversations")


def ensure_memory_dir():
    """Create the conversations directory if it doesn't exist."""
    os.makedirs(MEMORY_DIR, exist_ok=True)


def new_session():
    """Create a new conversation session, return its ID and file path."""
    ensure_memory_dir()
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(MEMORY_DIR, f"{session_id}.json")
    data = {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(),
        "messages": [],
    }
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    return session_id, filepath


def load_session(session_id):
    """Load an existing session's messages."""
    filepath = os.path.join(MEMORY_DIR, f"{session_id}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        return json.load(f)


def save_message(session_id, role, content):
    """Append a message to a session file."""
    filepath = os.path.join(MEMORY_DIR, f"{session_id}.json")
    with open(filepath, "r") as f:
        data = json.load(f)
    data["messages"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    })
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def list_sessions():
    """List all past conversation sessions."""
    ensure_memory_dir()
    sessions = []
    for filename in sorted(os.listdir(MEMORY_DIR), reverse=True):
        if filename.endswith(".json"):
            filepath = os.path.join(MEMORY_DIR, filename)
            with open(filepath, "r") as f:
                data = json.load(f)
            msg_count = len(data.get("messages", []))
            # Get first user message as preview
            preview = ""
            for msg in data.get("messages", []):
                if msg["role"] == "user":
                    preview = msg["content"][:60]
                    break
            sessions.append({
                "id": data["session_id"],
                "created": data["created_at"],
                "messages": msg_count,
                "preview": preview,
            })
    return sessions
