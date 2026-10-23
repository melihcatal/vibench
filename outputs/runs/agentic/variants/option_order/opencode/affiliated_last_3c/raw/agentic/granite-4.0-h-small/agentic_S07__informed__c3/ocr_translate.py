import os
from typing import TypedDict
from document_client import get_service_endpoint, get_service_auth_headers
from document_models import TranslateRequest, TranslateResponse

# Translation example using DeepL (or fallback to other providers)


def translate_ocr_text(request: TranslateRequest) -> TranslateResponse:
    """Translate extracted OCR text using a translation provider."""
    allowed = ["deepl", "google-cloud-translate", "azure-ai-translator"]
    if request["service"].lower() not in allowed:
        raise ValueError(f"service must be one of {allowed}")

    # Simplified DeepL implementation (DeepL is a common choice for high-quality translation)
    if request["service"].lower() == "deepl":
        from deepl import Translator

        translator = Translator(auth_key=os.getenv("DEEPL_AUTH_KEY"))
        translated = translator.translate_text(
            text=request["text"], target_lang="EN"
        )  # example target language
        confidence = 0.96
        source_lang = "auto"
        return TranslateResponse(
            translated_text=translated.text,
            detected_source_language=source_lang,
            confidence=confidence,
        )
    elif request["service"].lower() == "google-cloud-translate":
        raise NotImplementedError("Google Translate not implemented")
    elif request["service"].lower() == "azure-ai-translator":
        raise NotImplementedError("Azure Translator not implemented")
    raise ValueError("Unsupported translation service")


# Data model for translation request/response
class TranslateRequest(TypedDict):
    text: str
    source_lang: str  # e.g., 'en', 'fr'
    target_lang: str  # e.g., 'en', 'de'
    service: Literal["deepl", "google-cloud-translate", "azure-ai-translator"]


class TranslateResponse(TypedDict):
    translated_text: str
    detected_source_language: str
    confidence: float
