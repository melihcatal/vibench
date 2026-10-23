import os
from google.cloud import translate_v2 as translate

def translate_log_message(
    text: str,
    target_language: str,
    project_id: str = None
) -> str:
    """
    Translates support-visible log messages for another locale using Google Cloud Translation.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # or specify project_id if using API key with specific configuration
    client = translate.Client(project=project_id)

    # Text can also be a list of strings for batch translation
    result = client.translate(
        text,
        target_language=target_language
    )

    translated_text = result["translatedText"]
    print(f"Original: '{text}'")
    print(f"Translated to {target_language}: '{translated_text}'")
    return translated_text

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # For local testing, ensure you have authenticated with `gcloud auth application-default login`
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")

    english_message = "Failed to connect to the database. Please check network connectivity."
    spanish_translation = translate_log_message(english_message, "es", project_id=project_id)

    print("\n---")
    german_message = "Datenbankverbindung fehlgeschlagen."
    english_translation = translate_log_message(german_message, "en", project_id=project_id)
