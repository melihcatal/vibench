import base64
import json
import urllib.request

from speech_client import auth_headers, openai_base_url, load_speech_config


def submit_transcription(audio_path: str) -> dict:
    cfg = load_speech_config()
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    payload = json.dumps(
        {
            "model": cfg.transcription_model,
            "input_audio": base64.b64encode(audio_bytes).decode("utf-8"),
            "input_audio_format": "mp3",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{openai_base_url()}/responses",
        data=payload,
        headers={**auth_headers(), "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))
