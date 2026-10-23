import requests

from speech_client import load_speech_config
from speech_models import normalize_segments


def poll_transcription(transcript_id: str):
    config = load_speech_config()
    headers = {"authorization": config.api_key}
    resp = requests.get(f"{config.base_url}/v2/transcript/{transcript_id}", headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") == "completed" and data.get("utterances"):
        data["utterances"] = normalize_segments(data["utterances"])
    return data
