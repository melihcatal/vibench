from typing import Dict, List
from translation_client import GoogleTranslationClient
from translation_models import TranslationRequest, normalize_language_code


def translate_dictionary_values(
    data: Dict[str, str], target_language: str, source_language: str = None
) -> Dict[str, str]:
    client = GoogleTranslationClient()
    target_language = normalize_language_code(target_language)
    source_language = (
        normalize_language_code(source_language) if source_language else None
    )

    texts = list(data.values())
    requests = [
        TranslationRequest(
            text=text, target_language=target_language, source_language=source_language
        )
        for text in texts
    ]
    responses = client.batch_translate_text(requests)

    translated_data = {}
    for (key, _), response in zip(data.items(), responses):
        translated_data[key] = response.translated_text

    return translated_data
