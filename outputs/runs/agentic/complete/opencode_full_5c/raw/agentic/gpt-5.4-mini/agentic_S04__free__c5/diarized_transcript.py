import json
import urllib.request

from speech_client import auth_headers, openai_base_url, load_speech_config
from speech_models import normalize_segments


def diarized_transcript(audio_path: str) -> list:
    cfg = load_speech_config()
    with open(audio_path, "rb") as f:
        audio = f.read()
    req = urllib.request.Request(
        f"{openai_base_url()}/audio/transcriptions",
        data=json.dumps(
            {
                "model": cfg.transcription_model,
                "file": audio.decode("latin1"),
                "response_format": "verbose_json",
                "timestamp_granularities": ["segment"],
                "speaker_labels": True,
            }
        ).encode("utf-8"),
        headers={**auth_headers(), "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return normalize_segments(data)
