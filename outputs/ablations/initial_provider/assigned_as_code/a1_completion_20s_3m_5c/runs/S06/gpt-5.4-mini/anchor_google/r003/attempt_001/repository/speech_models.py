from dataclasses import dataclass


def normalize_language_code(value, default="en-US"):
    if not value:
        return default
    value = str(value).replace("_", "-").strip()
    if len(value) == 2:
        return value.lower()
    if len(value) == 5 and value[2] == "-":
        return value[:2].lower() + "-" + value[3:].upper()
    return value


def normalize_payload(payload):
    payload = dict(payload or {})
    payload["text"] = payload.get("text", "")
    payload["ssml"] = payload.get("ssml")
    payload["language_code"] = normalize_language_code(payload.get("language_code"))
    return payload


@dataclass
class SpeechRequest:
    text: str = ""
    ssml: str = ""
    language_code: str = "en-US"
    voice_name: str = ""
    speaking_rate: float = 1.0
    pitch: float = 0.0


@dataclass
class SpeechResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
