from google.cloud import translate_v2 as translate
from typing import Dict, Any

def localized_platform_output(project_id: str, text: str, target_language_code: str, source_language_code: str = "en") -> Dict[str, Any]:
    """Translates platform model output to a specified target language using Google Cloud Translation API.

    Args:
        project_id: Your Google Cloud project ID.
        text: The text to be translated.
        target_language_code: The BCP-47 language code of the target language (e.g., 'es' for Spanish).
        source_language_code: The BCP-47 language code of the source language (e.g., 'en' for English).

    Returns:
        A dictionary containing the translated text and translation metadata.
    """
    translate_client = translate.Client(project=project_id)

    print(f"Translating text from {source_language_code} to {target_language_code}...")
    print(f"Original text: {text}")

    # Target language can be specified as a string.
    response = translate_client.translate(
        text,
        target_language=target_language_code,
        source_language=source_language_code
    )

    translated_text = response['translatedText']
    detected_source_language = response.get('detectedSourceLanguage', source_language_code)

    translation_metadata = {
        "original_text": text,
        "translated_text": translated_text,
        "source_language": detected_source_language,
        "target_language": target_language_code,
        "provider": "Google Cloud Translation API"
    }

    print(f"Translated text: {translated_text}")
    print(f"Detected source language: {detected_source_language}")

    return translation_metadata

if __name__ == '__main__':
    # Replace with your actual project_id
    project_id = "your-gcp-project-id"
    output_text = "The quick brown fox jumps over the lazy dog. Generative AI is powerful."

    print("\n--- Translating to Spanish ---")
    spanish_translation = localized_platform_output(project_id, output_text, "es")
    print(spanish_translation)

    print("\n--- Translating to French ---")
    french_translation = localized_platform_output(project_id, "Hello, world!", "fr", "en")
    print(french_translation)

    print("\n--- Translating already Spanish text to English ---")
    spanish_input_to_english = localized_platform_output(project_id, "Hola mundo, la inteligencia artificial es genial.", "en", "es")
    print(spanish_input_to_english)
