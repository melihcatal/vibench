import os
from google.cloud import translate_v2 as translate


def translate_log_message(text: str, target_language: str = "fr") -> str:
    """
    Translates a log message to another language using Google Cloud Translation.

    Args:
        text: The log message to translate.
        target_language: The ISO 639-1 code for the target language.

    Returns:
        The translated text.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


if __name__ == "__main__":
    log_message_en = "INFO: User password has been reset successfully."

    # Translate to French
    translated_message_fr = translate_log_message(log_message_en, "fr")
    print(f"Original (en): {log_message_en}")
    print(f"Translated (fr): {translated_message_fr}")

    # Translate to Spanish
    translated_message_es = translate_log_message(log_message_en, "es")
    print(f"Translated (es): {translated_message_es}")
