import os
from typing import Optional
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
    model: str = "google-translate-v3",
    glossary_id: Optional[str] = None,
) -> str:
    """Translate a single text string using Google Cloud Translation API."""
    client = get_translation_client()
    request = TranslationRequest(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
        glossary_id=glossary_id,
    )
    response = client.translate_text(
        parent=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/global",
        contents=[request.text],
        source_language_code=request.source_lang,
        target_language_code=request.target_lang,
        model=request.model,
        glossary_config=request.glossary_config,
    )
    return TranslationResponse.from_google_response(response).translated_text