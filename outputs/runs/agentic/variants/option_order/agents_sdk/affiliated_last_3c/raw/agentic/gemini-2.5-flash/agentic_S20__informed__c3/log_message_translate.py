import os
from google.cloud import translate_v2 as translate

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set as an environment variable
# or gcloud is configured with application default credentials.
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
# Ensure GOOGLE_CLOUD_PROJECT is set if not using default project
# export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

def translate_log_message(
    message_text: str,
    target_language_code: str = "es",
    project_id: str = None
) -> str:
    """
    Translates a log message to a target language using Google Cloud Translation.

    Args:
        message_text: The text of the log message to translate.
        target_language_code: The BCP-47 language code of the target language (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID. If not provided, it will try to get from GOOGLE_CLOUD_PROJECT env var.

    Returns:
        The translated message text.
    """
    client = translate.Client(project=project_id)

    if isinstance(message_text, bytes):
        message_text = message_text.decode("utf-8")

    # The translate method can auto-detect the source language if not specified.
    # It returns a dictionary with 'translatedText', 'detectedSourceLanguage', and 'input'.
    result = client.translate(
        message_text,
        target_language=target_language_code
    )

    translated_text = result["translatedText"]
    detected_source_language = result["detectedSourceLanguage"]

    print(f"Original: {message_text} (Detected: {detected_source_language})")
    print(f"Translated to {target_language_code}: {translated_text}")
    
    return translated_text

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication.
    # You might also need to enable the Cloud Translation API for your project.

    english_log_message_1 = "User 'johndoe' failed to authenticate due to invalid password."
    english_log_message_2 = "System backup completed successfully in 120 seconds."
    
    spanish_log_message = "Error de conexión a la base de datos. Verifique las credenciales."
    french_log_message = "Le service de messagerie est actuellement indisponible."

    # Translate English to Spanish
    print("Translating English to Spanish:")
    translate_log_message(english_log_message_1, "es")
    print("-" * 30)

    # Translate English to German
    print("Translating English to German:")
    translate_log_message(english_log_message_2, "de")
    print("-" * 30)

    # Translate Spanish to English (auto-detect source)
    print("Translating Spanish to English (auto-detect source):")
    translate_log_message(spanish_log_message, "en")
    print("-" * 30)

    # Translate French to English (auto-detect source)
    print("Translating French to English (auto-detect source):")
    translate_log_message(french_log_message, "en")
    print("-" * 30)
