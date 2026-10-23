from typing import Dict, Any
from translation_client import get_deepl_translator
from translation_models import TranslationRequest, TranslationResponse


def translate_dictionary_values(
    data: Dict[str, str], target_lang: str, source_lang: str = None
) -> Dict[str, str]:
    translator = get_deepl_translator()
    translated_data = {}
    texts_to_translate = list(data.values())

    if not texts_to_translate:
        return translated_data

    # DeepL's translate_text can handle a list of strings
    results = translator.translate_text(
        texts_to_translate, target_lang=target_lang, source_lang=source_lang
    )

    # Reconstruct the dictionary with translated values
    keys = list(data.keys())
    for i, result in enumerate(results):
        translated_data[keys[i]] = result.text

    return translated_data
