import os
import deepl

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_API_URL = "https://api.deepl.com/v2/translate"

ONBOARDING_COPY = {
    "welcome_title": "Welcome to Our Platform",
    "welcome_body": "We are excited to have you on board. Complete your profile to get started.",
    "next_steps": "Next, verify your email and set up two-factor authentication.",
    "support_message": "Need help? Contact our support team anytime.",
}


def translate_onboarding(target_locale: str, copy: dict = None) -> dict:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(DEEPL_AUTH_KEY)

    source_copy = copy or ONBOARDING_COPY

    target_lang = target_locale.split("-")[0].upper()

    translated = {}
    for key, text in source_copy.items():
        result = translator.translate_text(
            text,
            target_lang=target_lang,
            source_lang="EN",
        )
        translated[key] = result.text

    return translated


def translate_single_text(
    text: str, target_locale: str, source_lang: str = "EN"
) -> str:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(DEEPL_AUTH_KEY)
    target_lang = target_locale.split("-")[0].upper()

    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
    )
    return result.text


if __name__ == "__main__":
    import sys

    locale = sys.argv[1] if len(sys.argv) > 1 else "es"
    result = translate_onboarding(locale)
    for key, value in result.items():
        print(f"{key}: {value}")
