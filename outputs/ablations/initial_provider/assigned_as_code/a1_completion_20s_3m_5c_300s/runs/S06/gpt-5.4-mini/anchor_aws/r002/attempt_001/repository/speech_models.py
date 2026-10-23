def normalize_text_payload(payload):
    return {"text": payload["text"].strip()}


def normalize_ssml_payload(payload):
    data = {"ssml": payload["ssml"].strip()}
    if "voice_id" in payload:
        data["voice_id"] = payload["voice_id"]
    if "rate" in payload:
        data["rate"] = payload["rate"]
    if "pitch" in payload:
        data["pitch"] = payload["pitch"]
    return data


def audio_response(audio_bytes, content_type):
    return {"audio_bytes": audio_bytes, "content_type": content_type}
