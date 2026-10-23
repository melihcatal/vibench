import os
from google.cloud import translate_v3 as translate

# Configure Google Cloud Translation client
# GOOGLE_APPLICATION_CREDENTIALS environment variable should be set


def translate_log_message(
    text: str, target_language_code: str = "es", project_id: str = None
) -> str:
    """
    Translates support-visible log messages for another locale using Google Cloud Translation.
    """
    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            return "Error: Google Cloud project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set."

    if not text:
        return ""

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )

        if response.translations:
            return response.translations[0].translated_text
        else:
            return "Translation failed: No translations returned."
    except Exception as e:
        return f"Error during translation: {e}"


if __name__ == "__main__":
    # Example usage
    log_message = "Failed to connect to the database. Please check your credentials."
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")  # Replace with your GCP Project ID

    translated_message_es = translate_log_message(
        log_message, target_language_code="es", project_id=project_id
    )
    print(f"Original (en): {log_message}")
    print(f"Translated (es): {translated_message_es}")

    print("\n" + "-" * 50 + "\n")

    log_message_de = "Benutzer 'admin' hat sich erfolgreich angemeldet."
    translated_message_en = translate_log_message(
        log_message_de, target_language_code="en", project_id=project_id
    )
    print(f"Original (de): {log_message_de}")
    print(f"Translated (en): {translated_message_en}")
