import os
from google.cloud import translate_v3 as translate

def translate_message_payload(project_id: str, text_content: str, target_language_code: str, source_language_code: str = None) -> dict:
    """Translates customer-facing message payload text using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"

    if source_language_code:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text_content],
                "target_language_code": target_language_code,
                "source_language_code": source_language_code,
            }
        )
    else:
        # Auto-detect source language if not provided
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text_content],
                "target_language_code": target_language_code,
            }
        )

    translations = []
    for translation in response.translations:
        translations.append({
            "translated_text": translation.translated_text,
            "detected_source_language": translation.detected_language_code,
            "model": translation.model,
        })

    print(f"Translation results: {translations}")
    return translations[0] if translations else {}

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        english_text = "Hello, how are you today? We have an important update for you."
        spanish_text = "Hola, ¿cómo estás hoy? Tenemos una actualización importante para ti."
        french_text = "Bonjour, comment allez-vous aujourd'hui ? Nous avons une mise à jour importante pour vous."

        print("\n--- Translating English to Spanish (auto-detect) ---")
        translate_message_payload(PROJECT_ID, english_text, "es")

        print("\n--- Translating English to French (explicit source) ---")
        translate_message_payload(PROJECT_ID, english_text, "fr", "en")

        print("\n--- Translating Spanish to English (auto-detect) ---")
        translate_message_payload(PROJECT_ID, spanish_text, "en")
