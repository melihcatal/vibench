# [LATER-STEP] localized_platform_output.py
# Translate watsonx model output to another locale using DeepL SDK

import os
from deepl import DeepL, TranslateParams
from typing import Dict


def translate_output(output: Dict[str, Any], target_lang: str = "de") -> Dict[str, Any]:
    """Translate the 'generated_text' field of a platform output to the target language.

    Returns a new dict with an additional 'translated_text' field.
    """
    deepl_api_key = os.getenv("DEEPL_AUTH_KEY")
    if not deepl_api_key:
        raise ValueError("Set DEEPL_AUTH_KEY environment variable")

    deepl = DeepL(deepl_api_key)
    translation = deepl.translate(
        text=output["generated_text"], target_lang=target_lang, params=TranslateParams()
    )
    translated_text = translation.translated_text

    return {
        **output,
        "translated_text": translated_text,
        "translation_target": target_lang,
    }
