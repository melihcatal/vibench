import os
from security_models import TranslationResult
from security_client import get_google_cloud_translation_client

def translate_compliance_note(text: str, target_language: str, source_language: str = "en") -> TranslationResult:
    """
    Translates an encryption or compliance note using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The language code for the target language (e.g., "es", "fr").
        source_language: The language code for the source language (defaults to "en").

    Returns:
        A TranslationResult object.
    """
    client = get_google_cloud_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Required for Cloud Translation v3
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set for Google Cloud Translation.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_text = ""
    detected_source_language = source_language
    if response.translations:
        translated_text = response.translations[0].translated_text
        # Google Cloud Translation automatically detects source language if not provided
        # The detected language can be found in the response if auto-detected
        if not source_language: # If source was not explicitly provided, try to get from response
            detected_source_language = response.translations[0].detected_language_code


    return TranslationResult(
        original_text=text,
        translated_text=translated_text,
        source_language=detected_source_language,
        target_language=target_language
    )

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT)
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

    # note_english = "The encryption keys are rotated quarterly as per compliance policy."
    # note_spanish = "Las claves de cifrado se rotan trimestralmente según la política de cumplimiento."

    # print(f"Translating English note: '{note_english}' to Spanish")
    # try:
    #     translation_to_es = translate_compliance_note(note_english, "es")
    #     print(f"  Translated to Spanish: {translation_to_es.translated_text}")
    #     print(f"  Source: {translation_to_es.source_language}, Target: {translation_to_es.target_language}")
    # except Exception as e:
    #     print(f"Error translating to Spanish: {e}")
    # print("-" * 30)

    # print(f"Translating Spanish note: '{note_spanish}' to English")
    # try:
    #     translation_to_en = translate_compliance_note(note_spanish, "en", source_language="es")
    #     print(f"  Translated to English: {translation_to_en.translated_text}")
    #     print(f"  Source: {translation_to_en.source_language}, Target: {translation_to_en.target_language}")
    # except Exception as e:
    #     print(f"Error translating to English: {e}")
