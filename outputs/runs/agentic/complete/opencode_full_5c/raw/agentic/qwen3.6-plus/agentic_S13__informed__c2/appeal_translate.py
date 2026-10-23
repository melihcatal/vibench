import os

import deepl


def translate_appeal(
    appeal_text: str,
    target_language: str = "EN-US",
    source_language: str | None = None,
) -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable is required. "
            "Set it to your DeepL API authentication key."
        )

    translator = deepl.Translator(auth_key)

    translate_kwargs = {}
    if source_language:
        translate_kwargs["source_lang"] = source_language

    result = translator.translate_text(
        appeal_text,
        target_lang=target_language,
        **translate_kwargs,
    )

    return result.text
