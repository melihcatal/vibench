import os
from typing import List, Optional
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def batch_translate(
    texts: List[str],
    source_lang: str,
    target_lang: str,
    model: str = "google-translate-v3",
    glossary_id: Optional[str] = None,
) -> List[str]:
    """Translate a list of strings while preserving order using Google Cloud Translation API."""
    client = get_translation_client()
    request = TranslationRequest(
        text="",
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
        glossary_id=glossary_id,
    )
    response = client.translate_text(
        parent=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/global",
        contents=texts,
        source_language_code=request.source_lang,
        target_language_code=request.target_lang,
        model=request.model,
        glossary_config=request.glossary_config,
    )
    return [
        TranslationResponse.from_google_response(r).translated_text
        for r in response.translations
    ]