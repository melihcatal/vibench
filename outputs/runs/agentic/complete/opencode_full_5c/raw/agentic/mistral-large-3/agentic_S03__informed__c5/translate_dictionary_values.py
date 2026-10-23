from typing import Dict, List, Optional
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_dictionary_values(
    dictionary: Dict[str, str],
    source_lang: str,
    target_lang: str,
    category: Optional[str] = None,
) -> Dict[str, str]:
    """
    Translates dictionary values while preserving keys using Azure AI Translator.
    """
    texts = list(dictionary.values())
    if not texts:
        return dictionary

    client = get_translation_client()
    request = TranslationRequest(
        texts=texts,
        source_language=source_lang,
        target_languages=[target_lang],
        category=category,
    )

    response = client.translate(request)
    translated_texts = response.translations[target_lang]

    return {
        key: translated_text
        for key, translated_text in zip(dictionary.keys(), translated_texts)
    }
