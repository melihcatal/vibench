import base64


def normalize_audio_chunks(audio_chunks):
    normalized = []
    for chunk in audio_chunks:
        if isinstance(chunk, str):
            normalized.append(base64.b64decode(chunk))
        else:
            normalized.append(chunk)
    return normalized


def normalize_language_code(language_code):
    return (language_code or "en-US").replace("_", "-")


def build_stream_payload(audio_chunks, language_code, sample_rate_hz=16000, **extra):
    payload = {
        "audio_chunks": normalize_audio_chunks(audio_chunks),
        "language_code": normalize_language_code(language_code),
        "sample_rate_hz": sample_rate_hz,
    }
    payload.update(extra)
    return payload


def event_text(event):
    if not event:
        return ""
    if isinstance(event, dict):
        return event.get("text", "")
    return getattr(event, "text", "")
