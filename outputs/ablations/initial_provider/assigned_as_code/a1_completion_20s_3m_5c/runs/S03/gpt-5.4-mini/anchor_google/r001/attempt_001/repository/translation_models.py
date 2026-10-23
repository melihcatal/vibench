from dataclasses import dataclass


def normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()


def normalize_payload(payload):
    payload = dict(payload or {})
    if "text" in payload:
        payload["text"] = normalize_text(payload["text"])
    if "texts" in payload:
        payload["texts"] = [normalize_text(item) for item in payload["texts"]]
    if "html" in payload:
        payload["html"] = normalize_text(payload["html"])
    if "source_language" in payload:
        payload["source_language"] = normalize_text(payload["source_language"])
    if "target_language" in payload:
        payload["target_language"] = normalize_text(payload["target_language"])
    return payload


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    text: str
    source_language: str
    target_language: str
