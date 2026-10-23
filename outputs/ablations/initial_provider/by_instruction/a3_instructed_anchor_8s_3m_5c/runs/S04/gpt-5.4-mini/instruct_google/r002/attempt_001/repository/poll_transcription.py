import json
import urllib.request

from speech_client import google_speech_headers, load_speech_config
from speech_models import transcript_text


def poll_transcription(operation_name: str):
    config = load_speech_config()
    url = f"https://speech.googleapis.com/v1/{operation_name}"
    req = urllib.request.Request(url, headers=google_speech_headers(config.google_api_key), method="GET")
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("done") and data.get("response"):
        return transcript_text(data["response"])
    return data
