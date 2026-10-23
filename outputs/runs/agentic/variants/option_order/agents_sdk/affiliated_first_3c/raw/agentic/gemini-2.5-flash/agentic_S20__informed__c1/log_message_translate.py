import os
from typing import Optional
from observability_client import get_translation_client, get_gcp_project_id
from observability_models import TranslationRequest

def translate_log_message(request: TranslationRequest) -> Optional[str]:
    """
    Translates support-visible log messages for another locale using Google Cloud Translation.
    """
    client = get_translation_client()
    project_id = get_gcp_project_id()

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    if not request.text_content:
        return None

    parent = f"projects/{project_id}/locations/global"

    print(f"Translating log message to {request.target_language_code}...")
    try:
        response = client.translate_text(
            request=translate.TranslateTextRequest(
                parent=parent,
                contents=[request.text_content],
                target_language_code=request.target_language_code,
                source_language_code=request.source_language_code,
            )
        )

        translated_text = response.translations[0].translated_text if response.translations else None
        print(f"Translation received: {translated_text}")
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication
    # Set GOOGLE_CLOUD_PROJECT_ID environment variable
    log_message = "Error: Failed to connect to the database. Please check network connectivity."

    translation_request_es = TranslationRequest(
        text_content=log_message,
        target_language_code="es",
        source_language_code="en"
    )

    translation_request_fr = TranslationRequest(
        text_content=log_message,
        target_language_code="fr",
    )

    print("\n--- Translating to Spanish ---")
    translated_es = translate_log_message(translation_request_es)
    if translated_es:
        print(f"Original (EN): {log_message}")
        print(f"Translated (ES): {translated_es}")

    print("\n--- Translating to French (auto-detect source) ---")
    translated_fr = translate_log_message(translation_request_fr)
    if translated_fr:
        print(f"Original: {log_message}")
        print(f"Translated (FR): {translated_fr}")
