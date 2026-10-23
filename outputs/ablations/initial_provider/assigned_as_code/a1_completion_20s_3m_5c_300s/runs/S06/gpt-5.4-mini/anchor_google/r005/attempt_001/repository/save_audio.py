from google.cloud import texttospeech

from speech_client import load_config


def save_audio(payload, config=None):
    config = load_config(config)
    audio = payload.get("audio_bytes", b"")
    path = payload.get("path")
    if path:
        with open(path, "wb") as f:
            f.write(audio)
        return {"path": path, "content_type": payload.get("content_type", "audio/mpeg")}
    return {"audio_bytes": audio, "content_type": payload.get("content_type", "audio/mpeg")}
