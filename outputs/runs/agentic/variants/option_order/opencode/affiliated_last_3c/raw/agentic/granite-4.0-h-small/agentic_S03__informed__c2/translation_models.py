from typing import Literal, TypedDict


class TranslationRequest(TypedDict):
    text: str
    source_lang: str
    target_lang: str


class TranslationResponse(TypedDict):
    translated_text: str
    detected_source_language: str


def normalize_request(req: dict) -> TranslationRequest:
    """Ensure request dict contains required fields."""
    return {
        "text": req.get("text", ""),
        "source_lang": req.get("source_lang", "EN"),
        "target_lang": req.get("target_lang", "FR"),
    }


def normalize_response(resp: Any) -> TranslationResponse:
    """Extract translated text and detected language."""
    return {
        "translated_text": getattr(resp, "translated_text", ""),
        "detected_source_language": getattr(resp, "detected_source_language", ""),
    }
