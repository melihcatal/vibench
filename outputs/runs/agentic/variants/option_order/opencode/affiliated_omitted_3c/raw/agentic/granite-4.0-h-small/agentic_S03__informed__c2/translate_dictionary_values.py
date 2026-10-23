import os
from typing import Dict, Any
from translate_text import translate_text

# Alibaba Machine Translation example
# Uses translate_text for individual string translation


def translate_dictionary_values(
    data: Dict[str, Any], source_lang: str = "en", target_lang: str = "zh"
) -> Dict[str, Any]:
    """Translate values of a dictionary while preserving keys.

    Non-string values are left unchanged.

    Args:
        data: Source dictionary.
        source_lang: Language code of the source values.
        target_lang: Language code of the target language.

    Returns:
        New dictionary with translated values.
    """
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = translate_text(value, source_lang, target_lang)
        else:
            translated[key] = value  # non-string values unchanged
    return translated


# Demo when executed directly
if __name__ == "__main__":
    sample_dict = {"greeting": "Hello, world!", "farewell": "Goodbye!"}
    print("Original dict:", sample_dict)
    print("Translated values:", translate_dictionary_values(sample_dict))
