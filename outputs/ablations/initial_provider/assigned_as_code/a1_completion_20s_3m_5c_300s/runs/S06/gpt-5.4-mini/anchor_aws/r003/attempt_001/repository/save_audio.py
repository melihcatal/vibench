from speech_models import normalize_text_payload


def save_audio(payload, config=None):
    payload = normalize_text_payload(payload)
    audio_bytes = payload["audio_bytes"]
    target = payload.get("path") or payload.get("file_path")
    if target:
        with open(target, "wb") as handle:
            handle.write(audio_bytes)
        return {"path": target, "content_type": payload.get("content_type", "audio/mpeg")}
    return {"audio_bytes": audio_bytes, "content_type": payload.get("content_type", "audio/mpeg")}
