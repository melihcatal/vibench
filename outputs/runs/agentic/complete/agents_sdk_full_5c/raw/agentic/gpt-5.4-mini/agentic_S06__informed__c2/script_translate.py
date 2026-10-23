from __future__ import annotations

from typing import Optional

from google.cloud import translate_v2 as translate

from speech_models import TranslationRequest, TranslationResponse, normalize_text

GOOGLE_TRANSLATE_CLIENT = "google-cloud-translate"


def translate_script(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    request = TranslationRequest(text=normalize_text(text), target_language=target_language, source_language=source_language)
    client = translate.Client()
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )
    TranslationResponse(text=result["translatedText"], provider=GOOGLE_TRANSLATE_CLIENT, metadata={"request": request.__dict__})
    return result["translatedText"]
