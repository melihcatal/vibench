from translation_client import get_deepl_translator
from typing import Dict, Any, Optional


def translate_dictionary_values(
    data: Dict[str, Any], target_lang: str, source_lang: Optional[str] = None
) -> Dict[str, Any]:
    translator = get_deepl_translator()
    translated_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            result = translator.translate_text(
                value, target_lang=target_lang, source_lang=source_lang
            )
            if isinstance(result, list):
                translated_data[key] = result[0].text
            else:
                translated_data[key] = result.text
        else:
            translated_data[key] = value
    return translated_data
