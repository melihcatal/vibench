
from google.cloud import translate_v3 as translate

def translate_log_message(text: str, project_id: str, target_language: str = "es") -> str:
    """Translates a log message into the target language using Google Cloud Translation.
    
    Args:
        text: The log message to translate.
        project_id: The Google Cloud project ID.
        target_language: The language to translate the message into (e.g., "es" for Spanish).

    Returns:
        The translated log message.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en", # Assuming source language is English
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your actual Google Cloud Project ID
    # You would typically get this from an environment variable or configuration.
    # For demonstration, we'll use a placeholder.
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Or, if using Application Default Credentials, it might be automatically detected.
    project_id = "your-gcp-project-id"  

    log_message = "User 'johndoe' failed to authenticate due to invalid password."
    translated_message = translate_log_message(log_message, project_id, "es")
    print(f"Original: {log_message}")
    print(f"Translated (es): {translated_message}")

    translated_message_fr = translate_log_message(log_message, project_id, "fr")
    print(f"Translated (fr): {translated_message_fr}")
