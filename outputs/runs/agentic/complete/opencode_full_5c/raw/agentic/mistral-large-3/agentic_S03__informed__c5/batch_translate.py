from typing import List, Optional
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def batch_translate(
    texts: List[str],
    source_lang: str,
    target_lang: str,
    category: Optional[str] = None,
) -> List[str]:
    """
    Translates a list of strings while preserving order using Azure AI Translator.
    """
    client = get_translation_client()

    request = TranslationRequest(
        texts=texts,
        source_language=source_lang,
        target_languages=[target_lang],
        category=category,
    )

    response = client.translate(request)
    return response.translations[target_lang]
