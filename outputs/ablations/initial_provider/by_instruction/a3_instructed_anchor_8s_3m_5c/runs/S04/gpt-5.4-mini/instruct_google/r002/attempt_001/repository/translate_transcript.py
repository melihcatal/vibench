import json
import urllib.request

from speech_client import load_speech_config


def translate_transcript(text: str, target_language: str = "en"):
    config = load_speech_config()
    payload = {
        "model": config.openai_model,
        "messages": [
            {"role": "system", "content": "Translate transcript segments faithfully."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {config.openai_api_key or ''}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))
