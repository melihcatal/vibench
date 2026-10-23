def normalize_text_payload(payload):
    if isinstance(payload, dict):
        return payload.get("text", "")
    return str(payload)


def normalize_ssml_payload(payload):
    if isinstance(payload, dict):
        return payload.get("ssml", payload.get("text", ""))
    return str(payload)


def build_audio_response(audio_bytes, content_type="audio/mpeg"):
    return {"audio_bytes": audio_bytes, "content_type": content_type}
