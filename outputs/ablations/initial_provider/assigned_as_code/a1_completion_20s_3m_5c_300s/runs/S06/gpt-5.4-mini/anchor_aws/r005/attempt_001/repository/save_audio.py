from speech_client import load_config


def save_audio(payload, config=None):
    cfg = load_config(config)
    audio_bytes = payload.get("audio_bytes", b"")
    path = (payload or {}).get("path") or cfg.get("path")
    if path:
        with open(path, "wb") as f:
            f.write(audio_bytes)
        return {"path": path, "content_type": payload.get("content_type", "audio/mpeg")}
    return {"audio_bytes": audio_bytes, "content_type": payload.get("content_type", "audio/mpeg")}
