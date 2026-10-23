import os
from google.cloud import translate_v2 as translate

# Assuming `model_models` is available in the local environment
from model_models import TranslatedOutput

def translate_text(text: str, target_language_code: str, project_id: str = None) -> TranslatedOutput:
    # Initialize Google Cloud Translation client
    # The client automatically uses GOOGLE_APPLICATION_CREDENTIALS or default credentials
    client = translate.Client(project=project_id)

    # Detect source language (optional, but good practice)
    detection = client.detect_language(text)
    source_language_code = detection['language']

    result = client.translate(text, target_language=target_language_code, source_language=source_language_code)

    translated_text = result['translatedText']
    
    return TranslatedOutput(
        translated_text=translated_text,
        source_language=source_language_code,
        target_language=target_language_code,
        raw_response=result
    )

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Ensure this env var is set or pass it directly
    if not project_id:
        print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Translation might fail without proper authentication.")

    text_to_translate = "Hello World, how are you today?"
    target_locale = "es"
    
    try:
        print(f"\nTranslating: '{text_to_translate}' to '{target_locale}'")
        translation_result = translate_text(text_to_translate, target_locale, project_id=project_id)
        print(f"Original ({translation_result.source_language}): {text_to_translate}")
        print(f"Translated ({translation_result.target_language}): {translation_result.translated_text}")
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        print("Please ensure Google Cloud Translation API is enabled and GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT is set.")
