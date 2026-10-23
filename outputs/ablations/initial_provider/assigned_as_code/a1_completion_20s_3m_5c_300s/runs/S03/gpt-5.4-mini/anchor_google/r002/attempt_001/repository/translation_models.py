from dataclasses import dataclass


def normalize_language_code(value):
    return value.replace("_", "-").lower() if isinstance(value, str) else value


def normalize_text_value(value):
    return "" if value is None else str(value)


def normalize_payload(payload):
    return {
        "text": normalize_text_value(payload.get("text")),
        "source_language": normalize_language_code(payload.get("source_language")),
        "target_language": normalize_language_code(payload.get("target_language")),
    }


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
