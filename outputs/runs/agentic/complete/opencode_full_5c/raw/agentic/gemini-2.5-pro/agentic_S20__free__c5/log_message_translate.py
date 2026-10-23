import os
from google.cloud import translate_v2 as translate


def translate_log_message(text: str, target_locale: str) -> str:
    """
    Translates a log message to a specified locale using Google Cloud Translation.
    """
    # Requires authentication, e.g., `gcloud auth application-default login`
    # and GOOGLE_CLOUD_PROJECT to be set.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_locale)

    return result["translatedText"]


if __name__ == "__main__":
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        log_message_en = "Error: User is not authorized to access this resource."
        target_language = "es"  # Spanish

        translated_message = translate_log_message(log_message_en, target_language)

        print(f"Original message (en): {log_message_en}")
        print(f"Translated message ({target_language}): {translated_message}")

        log_message_en_2 = "Customer support ticket has been updated."
        target_language_2 = "ja"  # Japanese

        translated_message_2 = translate_log_message(
            log_message_en_2, target_language_2
        )

        print(f"Original message (en): {log_message_en_2}")
        print(f"Translated message ({target_language_2}): {translated_message_2}")
