import os
import requests
from messaging_models import prepare_dead_letter

TISANE_API_KEY = os.getenv('TISANE_API_KEY')
TISANE_ENDPOINT = 'https://api.tisane.ai/v1/analyze'

def check_unsafe_content(payload: dict) -> bool:
    """Check whether the message payload contains unsafe language.

    Uses Tisane Text Moderation API. Returns True if unsafe, False otherwise.
    """
    if not TISANE_API_KEY:
        raise RuntimeError('TISANE_API_KEY not set')
    headers = {
        'Authorization': f'Bearer {TISANE_API_KEY}',
        'Content-Type': 'application/json'
    }
    # Tisane expects text in field 'text'
    text = payload.get('text')
    if not text:
        return False  # Nothing to moderate
    body = {'text': text}
    resp = requests.post(TISANE_ENDPOINT, headers=headers, json=body)
    if resp.status_code != 200:
        # Treat non‑200 as failure to moderate – treat as safe to avoid blocking
        print(f"Tisane moderation error {resp.status_code}: {resp.text}")
        return False
    data = resp.json()
    # Simple heuristic: if 'unsafe' flag present and true, treat as unsafe
    unsafe_flag = data.get('mods', {}).get('unsafe')
    unsafe = unsafe_flag if isinstance(unsafe_flag, bool) else False
    if unsafe:
        msg_id = payload.get('message_id')
        print(f"Unsafe content detected (msg_id={msg_id}).")
        return True
    return False

def handle_unsafe(payload: dict, error_msg: str) -> None:
    """Send an unsafe payload (or a rejection notice) to a dead‑letter topic.
    """
    dl = prepare_dead_letter(payload, error_msg)
    # Reuse publish helper from messaging_client (you could import here)
    from messaging_client import get_publisher_client
    publisher = get_publisher_client()
    topic = os.getenv('DEAD_LETTER_TOPIC', 'dead-letter-topic')
    publisher.publish(topic, data=str(dl).encode('utf-8'))
