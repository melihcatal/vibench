from google.cloud import translate_v2 as translate
import os


def translate_log_message(log_message, target_language_code):
    """
    Translates support-visible log messages for another locale using Google Cloud Translation.
    """
    client = translate.Client()

    # The Google Cloud Translation API requires a project ID to be set either
    # through the GOOGLE_CLOUD_PROJECT environment variable or
    # by initializing the client with project=YOUR_PROJECT_ID.
    # Assuming GOOGLE_APPLICATION_CREDENTIALS or default credentials are set up.

    result = client.translate(log_message, target_language=target_language_code)
    return result["translatedText"]


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication.
    # message_to_translate = "Error de conexión a la base de datos."
    # translated_message = translate_log_message(message_to_translate, "en")
    # print(f"Original: {message_to_translate}")
    # print(f"Translated (en): {translated_message}")
    pass
