def save_audio(payload, config=None):
    config = config or {}
    path = config.get("path")
    if path:
        with open(path, "wb") as f:
            f.write(payload["audio_bytes"])
        return {"path": path, "content_type": payload.get("content_type", "audio/mpeg")}
    return {"audio_bytes": payload["audio_bytes"], "content_type": payload.get("content_type", "audio/mpeg")}
