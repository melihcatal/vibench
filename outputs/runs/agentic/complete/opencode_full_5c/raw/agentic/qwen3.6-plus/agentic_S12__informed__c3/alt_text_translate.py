import os

import deepl

from vision_models import TranslatedAltText


def translate_alt_text(alt_text: str, target_language: str = "ES") -> TranslatedAltText:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        alt_text,
        target_lang=target_language,
    )

    return TranslatedAltText(
        original=alt_text,
        translated=result.text,
        target_language=target_language,
    )
