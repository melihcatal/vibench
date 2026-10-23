import os
import deepl


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_welcome_text(
    text: str, target_locale: str, source_locale: str = "en"
) -> str:
    if not DEEPL_AUTH_KEY:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable is required for DeepL translation"
        )

    target_lang = target_locale.split("-")[0].upper()
    source_lang = source_locale.split("-")[0].upper()

    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(
        text,
        source_lang=source_lang,
        target_lang=target_lang,
    )

    return result.text


def translate_onboarding_bundle(
    bundle: dict, target_locale: str, source_locale: str = "en"
) -> dict:
    translated = {}
    for key, value in bundle.items():
        if isinstance(value, str) and value.strip():
            translated[key] = translate_welcome_text(
                value, target_locale, source_locale
            )
        else:
            translated[key] = value
    return translated
