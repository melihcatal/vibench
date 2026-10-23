from pathlib import Path


def save_audio(payload, config=None):
    payload = payload or {}
    audio_bytes = payload["audio_bytes"]
    destination = payload.get("path") or (config or {}).get("path")
    if destination:
        path = Path(destination)
        path.write_bytes(audio_bytes)
        return {"path": str(path), "content_type": payload.get("content_type", "audio/mpeg")}
    return {"audio_bytes": audio_bytes, "content_type": payload.get("content_type", "audio/mpeg")}
