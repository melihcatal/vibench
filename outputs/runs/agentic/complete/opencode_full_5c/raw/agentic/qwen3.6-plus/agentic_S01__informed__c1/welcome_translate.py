import os
import deepl
from identity_models import TranslationResult


ONBOARDING_COPY = {
    "welcome_title": "Welcome to our platform",
    "welcome_body": "We are excited to have you on board. Let's get started with setting up your profile.",
    "next_steps": "Complete your profile, verify your email, and explore our features.",
    "support_message": "Need help? Our support team is here for you 24/7.",
}


def translate_onboarding_copy(
    target_language: str = "en-US",
    source_language: str = "auto",
    auth_key: str = None,
) -> dict:
    auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    translated = {}
    for key, text in ONBOARDING_COPY.items():
        result = translator.translate_text(
            text,
            target_lang=target_language.split("-")[0].upper(),
            source_lang=source_language if source_language != "auto" else None,
        )
        translated[key] = result.text

    return translated


def translate_text(
    text: str,
    target_language: str = "en-US",
    source_language: str = "auto",
    auth_key: str = None,
) -> TranslationResult:
    auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    deepl_result = translator.translate_text(
        text,
        target_lang=target_language.split("-")[0].upper(),
        source_lang=source_language if source_language != "auto" else None,
    )

    return TranslationResult(
        original_text=text,
        translated_text=deepl_result.text,
        source_language=deepl_result.detected_source_lang or source_language,
        target_language=target_language,
    )


if __name__ == "__main__":
    result = translate_onboarding_copy(target_language="es")
    print(result)
