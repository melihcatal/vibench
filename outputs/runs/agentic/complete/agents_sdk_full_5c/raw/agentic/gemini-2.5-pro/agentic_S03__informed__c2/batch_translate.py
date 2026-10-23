from typing import List
from translation_client import get_translation_client
from translation_models import TranslationResponse, BatchTranslationResponse

def batch_translate_texts(
    texts: List[str], target_language: str, source_language: str = None
) -> BatchTranslationResponse:
    """
    Translates a list of text strings in a single batch request.

    Args:
        texts: A list of strings to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language. Optional.

    Returns:
        A BatchTranslationResponse object with a list of translation results.
    """
    if not texts:
        return BatchTranslationResponse(translations=[])

    client = get_translation_client()

    results = client.translate(
        texts,
        target_language=target_language,
        source_language=source_language or '',
    )

    translated_responses = [
        TranslationResponse(
            translated_text=item['translatedText'],
            detected_source_language=item.get('detectedSourceLanguage'),
            original_text=item['input']
        ) for item in results
    ]

    return BatchTranslationResponse(translations=translated_responses)
