from speech_client import load_config


def save_audio(payload, config=None):
    cfg = load_config(config)
    audio_bytes = payload["audio_bytes"]
    target = payload["path"]
    if hasattr(target, "write"):
        target.write(audio_bytes)
        return {"written": len(audio_bytes), "content_type": payload.get("content_type", f"audio/{cfg['output_format']}")}
    with open(target, "wb") as handle:
        handle.write(audio_bytes)
    return {"path": target, "written": len(audio_bytes), "content_type": payload.get("content_type", f"audio/{cfg['output_format']}")}
