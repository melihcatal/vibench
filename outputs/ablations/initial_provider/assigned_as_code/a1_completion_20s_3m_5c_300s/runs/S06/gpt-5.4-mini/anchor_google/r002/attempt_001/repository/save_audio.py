def save_audio(payload, config=None):
    config = config or {}
    audio_bytes = payload.get("audio_bytes", b"")
    path = config.get("path") or payload.get("path")
    if path:
        with open(path, "wb") as file:
            file.write(audio_bytes)
        return {"path": path, "content_type": payload.get("content_type", "audio/mpeg")}
    return {"audio_bytes": audio_bytes, "content_type": payload.get("content_type", "audio/mpeg")}
