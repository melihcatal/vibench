import os

import deepl

from model_models import TranslationResponse


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def translate_text(
    text: str,
    target_language: str = "EN",
    source_language: str | None = None,
) -> TranslationResponse:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(DEEPL_AUTH_KEY)

    kwargs = {}
    if source_language:
        kwargs["source_lang"] = source_language
    kwargs["target_lang"] = target_language

    result = translator.translate_text(text, **kwargs)

    detected_source = (
        result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else "auto"
    )

    return TranslationResponse(
        translated_text=result.text,
        source_language=detected_source,
        target_language=target_language,
        metadata={"deepl_model": "deepl-translator-v2"},
    )


def translate_generated_output(
    text: str,
    target_language: str = "EN",
) -> TranslationResponse:
    return translate_text(text, target_language=target_language)


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    result = translate_text(input_text)
    print(result.translated_text)
