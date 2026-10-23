def normalize_text_payload(payload):
    if isinstance(payload, str):
        return {"text": payload}
    return dict(payload or {})


def normalize_ssml_payload(payload):
    data = dict(payload or {})
    if "ssml" not in data and "text" in data:
        data["ssml"] = data["text"]
    return data


def audio_response(audio_bytes, content_type="audio/mpeg", **extra):
    result = {"audio_bytes": audio_bytes, "content_type": content_type}
    result.update(extra)
    return result
