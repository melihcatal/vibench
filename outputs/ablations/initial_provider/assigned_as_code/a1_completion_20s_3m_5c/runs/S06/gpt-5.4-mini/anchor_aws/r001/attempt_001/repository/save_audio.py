from pathlib import Path


def save_audio(payload, config=None):
    data = dict(payload or {})
    audio_bytes = data.get("audio_bytes", b"")
    target = data.get("path")
    if target:
        Path(target).write_bytes(audio_bytes)
        return {"path": target, "saved": True}
    return {"audio_bytes": audio_bytes, "content_type": data.get("content_type", "audio/mpeg")}
