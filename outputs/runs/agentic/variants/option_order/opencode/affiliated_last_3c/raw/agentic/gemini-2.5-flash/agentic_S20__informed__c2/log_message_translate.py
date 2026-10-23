import os
from google.cloud import translate


def translate_log_message(text: str, target_language: str = "es") -> str:
    """Translates support-visible log messages for another locale using Google Cloud Translation."""
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    # or the client will try to find default credentials.

    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        for translation in response.translations:
            return translation.translated_text
        return ""
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return f"Translation Error: {e}"


if __name__ == "__main__":
    # Example usage:
    english_message = "Failed to connect to the database. Retrying..."
    spanish_translation = translate_log_message(english_message, target_language="es")
    print(f"\nEnglish: {english_message}")
    print(f"Spanish: {spanish_translation}")

    german_message = "Benutzerauthentifizierung fehlgeschlagen."
    english_translation = translate_log_message(german_message, target_language="en")
    print(f"\nGerman: {german_message}")
    print(f"English: {english_translation}")
