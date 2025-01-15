# Developer: Eric Neftali Paiz
import os
import json
from datetime import datetime, timedelta

BASE_DIR = "data"
CHAT_LOGS_DIR = os.path.join(BASE_DIR, "chat_logs")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
UPLOADED_DIR = os.path.join(BASE_DIR, "uploaded")
TEMP_DIR = os.path.join(BASE_DIR, "temp")


os.makedirs(CHAT_LOGS_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(UPLOADED_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def clean_old_files(directory, days=7):
    now = datetime.now()
    cutoff = now - timedelta(days=days)
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if datetime.fromtimestamp(os.path.getmtime(file_path)) < cutoff:
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")


def create_unique_filename(base_dir, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    unique_name = filename
    while os.path.exists(os.path.join(base_dir, unique_name)):
        unique_name = f"{name}_{counter}{ext}"
        counter += 1
    return unique_name


### Chat History Management ###
def save_chat_history(session_id, chat_history):
    file_path = os.path.join(CHAT_LOGS_DIR, f"{session_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=4)
    print(f"Chat history saved to: {file_path}")


def load_chat_history(session_id):
    file_path = os.path.join(CHAT_LOGS_DIR, f"{session_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def prepare_ollama_prompt(base_prompt, user_message, conversation_history=None):
    """
    Constructs the full prompt for the Ollama API.

    Args:
        base_prompt (str): The initial system prompt for the chat.
        user_message (str): The user's current input.
        conversation_history (list): Optional list of previous exchanges.

    Returns:
        str: Complete prompt including history and user input.
    """
    print("Preparing Ollama prompt...")
    if not conversation_history:
        conversation_history = []
    
    conversation_text = "\n".join([f"{sender}: {message}" for sender, message in conversation_history])
    complete_prompt = f"{base_prompt}\n{conversation_text}\nUser: {user_message}\nBot:"
    print(f"Prepared prompt: {complete_prompt[:100]}...")  # Truncated for debugging
    return complete_prompt


def save_ollama_response(session_id, user_message, bot_response):
    """
    Logs the user input and bot response into the chat history.

    Args:
        session_id (str): Unique ID for the session.
        user_message (str): The user's message.
        bot_response (str): The bot's response.
    """
    print(f"Saving Ollama response for session {session_id}...")
    chat_history = load_chat_history(session_id)
    chat_history.append(("User", user_message))
    chat_history.append(("Bot", bot_response))
    save_chat_history(session_id, chat_history)


def retrieve_summary(session_id):
    """
    Retrieves the most recent summary generated in the session.

    Args:
        session_id (str): Unique ID for the session.

    Returns:
        str: The latest summary if available.
    """
    print(f"Retrieving summary for session {session_id}...")
    chat_history = load_chat_history(session_id)
    summaries = [msg for sender, msg in chat_history if sender == "Bot" and "Summary:" in msg]
    return summaries[-1] if summaries else "No summary available."

def clear_temp_files():
    for file in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, file)
        os.remove(file_path)
        print(f"Removed temp file: {file_path}")


