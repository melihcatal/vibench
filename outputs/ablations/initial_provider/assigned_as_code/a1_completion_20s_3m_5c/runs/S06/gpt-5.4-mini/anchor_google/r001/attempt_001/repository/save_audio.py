from pathlib import Path


def save_audio(payload, config=None):
    payload = dict(payload or {})
    config = dict(config or {})
    audio_bytes = payload.get("audio_bytes", b"")
    output_path = config.get("output_path")
    if output_path:
        Path(output_path).write_bytes(audio_bytes)
        return {"path": output_path, "content_type": payload.get("content_type", "audio/mpeg")}
    return {"audio_bytes": audio_bytes, "content_type": payload.get("content_type", "audio/mpeg")}
