import os
from observability_client import get_translate_client


def translate_log_message(text: str, target_language: str = "es") -> dict:
    """
    Translates support-visible log messages for another locale using Google Cloud Translation.
    """
    client = (
        get_translate_client()
    )  # google.cloud.translate_v2 is a provider-identifying signal

    # The Google Cloud Translation API automatically detects the source language.
    result = client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }


if __name__ == "__main__":
    message_en = "User authentication failed due to invalid credentials."
    message_es = translate_log_message(message_en, target_language="es")
    print(f"English: {message_en}")
    print(f"Translated (Spanish): {message_es['translated_text']}")

    message_fr = translate_log_message(message_en, target_language="fr")
    print(f"Translated (French): {message_fr['translated_text']}")

    message_jp = translate_log_message(
        "Database connection error: Timeout", target_language="ja"
    )
    print(f"Original: Database connection error: Timeout")
    print(f"Translated (Japanese): {message_jp['translated_text']}")
