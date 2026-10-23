from google.cloud import translate_v2 as translate
import os


def translate_log_message(text: str, target_language: str, project_id: str) -> dict:
    """Translates a log message using Google Cloud Translation API."""

    # The translate_v2 client doesn't require project_id at instantiation
    # but relies on ADC (Application Default Credentials) which uses the project.
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT must be set.")

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result


if __name__ == "__main__":
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if gcp_project_id:
        log_message_en = "Error: Unable to process payment. Please check card details."
        target_locale = "es"  # Spanish

        translation_result = translate_log_message(
            log_message_en, target_locale, gcp_project_id
        )

        print(f"Original ('en'): {log_message_en}")
        print(f"Translated ('{target_locale}'): {translation_result['translatedText']}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable is not set.")
