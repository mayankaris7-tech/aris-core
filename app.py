import requests
import json
import urllib.parse

# --- ZERO-KEY ARIS CORE (100% FREE PUBLIC NEURAL ROUTER) ---
def run_no_key_aris(query):
    memories = "\n".join([f"- {m}" for m in st.session_state.memory_vault]) or "None."
    system_prompt = f"You are ARIS // JARVIS, an elite AI assistant created by Mayank (Boss). Tone: Confident, witty, razor-sharp intelligence, addressing user as Boss or Sir. If prompt is in Hinglish or Hindi, reply in conversational Hinglish. If English, British Jarvis tone. Memory: {memories}"

    # Pollinations public OpenAI-compatible text endpoint (No API Key Required)
    url = "https://text.pollinations.ai/"
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        "model": "openai",
        "seed": 42,
        "jsonMode": False
    }

    try:
        response = requests.post(url, json=payload, timeout=25)
        if response.status_code == 200:
            return response.text
        else:
            return f"[CORE FAULT]: Server returned status {response.status_code}. Retry again."
    except Exception as e:
        return f"[SYSTEM ERROR]: Connection timeout - {str(e)}"
