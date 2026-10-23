from typing import Dict, Any

from translation_client import get_target_language_code, get_translator
from translation_models import normalize_mapping_values


def translate_dictionary_values(
    data: Dict[str, Any], source_language: str, target_language: str
) -> Dict[str, str]:
    translator = get_translator()
    normalized = normalize_mapping_values(data)
    return {
        key: str(
            translator.translate_text(
                value,
                source_lang=source_language,
                target_lang=get_target_language_code(target_language),
            ).text
        )
        for key, value in normalized.items()
    }
