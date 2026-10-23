import os
from google.cloud import translate_v2 as translate
from security_models import TranslatedText


def translate_runbook_text(text: str, target_language: str) -> TranslatedText:

    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set."
        )

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    try:
        result = translate_client.translate(text, target_language=target_language)
    except Exception as e:
        print(f"Error translating text with Google Cloud Translate: {e}")
        raise

    return TranslatedText(
        original_text=text,
        translated_text=result["translatedText"],
        target_language=target_language,
    )


if __name__ == "__main__":
    runbook_notes = os.environ.get(
        "RUNBOOK_TEXT",
        "In case of emergency, immediately rotate the database credentials.",
    )
    target_lang = os.environ.get("TARGET_LANGUAGE", "es")  # Spanish

    try:
        translation = translate_runbook_text(runbook_notes, target_lang)
        print(f"Original ('en'): {translation.original_text}")
        print(
            f"Translated ('{translation.target_language}'): {translation.translated_text}"
        )
    except ValueError as e:
        print(e)
