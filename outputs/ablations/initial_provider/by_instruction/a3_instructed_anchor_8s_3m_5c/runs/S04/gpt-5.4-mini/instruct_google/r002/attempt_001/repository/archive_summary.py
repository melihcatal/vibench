import json
import urllib.request

from speech_client import load_speech_config


def archive_summary(text: str):
    config = load_speech_config()
    payload = {
        "model": config.openai_model,
        "messages": [
            {"role": "system", "content": "Summarize transcription results for archival indexing."},
            {"role": "user", "content": text},
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
