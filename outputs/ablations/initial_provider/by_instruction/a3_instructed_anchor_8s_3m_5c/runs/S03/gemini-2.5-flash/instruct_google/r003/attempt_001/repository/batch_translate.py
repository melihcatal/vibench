from typing import List
from translation_client import get_translate_client
from translation_models import TranslationText, TargetLanguage, SourceLanguage, BatchTranslationResponse

def batch_translate(texts: List[TranslationText], target_language: TargetLanguage, source_language: SourceLanguage = None) -> BatchTranslationResponse:
    """Translates a list of text strings using Google Cloud Translation, preserving order.

    Args:
        texts: A list of text strings to translate.
        target_language: The language to translate the texts into.
        source_language: The language of the input texts. If not specified,
                         Google Cloud Translation will attempt to detect the source language for each text.

    Returns:
        A BatchTranslationResponse object containing a list of translated texts.
    """
    client = get_translate_client()
    translated_texts = []

    if source_language:
        results = client.translate(texts, target_language=target_language, source_language=source_language)
    else:
        results = client.translate(texts, target_language=target_language)

    for result in results:
        translated_texts.append(result['translatedText'])

    return BatchTranslationResponse(translated_texts=translated_texts)
