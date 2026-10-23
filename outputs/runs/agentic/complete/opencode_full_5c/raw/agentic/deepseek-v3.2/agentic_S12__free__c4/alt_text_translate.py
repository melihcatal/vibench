import os
from deep_translator import GoogleTranslator
from typing import Dict, Any


def translate_image_description(
    description: str, target_language: str = "es"
) -> Dict[str, Any]:
    """
    Translate generated image descriptions using Google Translate API.

    Args:
        description: Image description text to translate
        target_language: Target language code (default: Spanish 'es')

    Returns:
        Dictionary containing original and translated text
    """
    try:
        translator = GoogleTranslator(source="auto", target=target_language)
        translated_text = translator.translate(description)

        return {
            "original_text": description,
            "translated_text": translated_text,
            "target_language": target_language,
            "provider": "google-translate",
            "source_language": translator.source
            if hasattr(translator, "source")
            else "auto",
        }
    except Exception as e:
        raise Exception(f"Translation failed: {e}")


def translate_multiple_descriptions(
    descriptions: Dict[str, str], target_languages: list
) -> Dict[str, Any]:
    """
    Translate multiple image descriptions to multiple languages.

    Args:
        descriptions: Dictionary with description names as keys and text as values
        target_languages: List of target language codes

    Returns:
        Dictionary containing all translations
    """
    results = {}

    for desc_name, desc_text in descriptions.items():
        results[desc_name] = {}
        for lang in target_languages:
            try:
                translator = GoogleTranslator(source="auto", target=lang)
                translated = translator.translate(desc_text)
                results[desc_name][lang] = {
                    "translated": translated,
                    "provider": "google-translate",
                }
            except Exception as e:
                results[desc_name][lang] = {
                    "error": str(e),
                    "provider": "google-translate",
                }

    return {
        "translations": results,
        "provider": "google-translate",
        "target_languages": target_languages,
    }


if __name__ == "__main__":
    # Example usage
    sample_description = "A beautiful sunset over the ocean with orange and pink clouds"

    try:
        translation = translate_image_description(sample_description, "fr")
        print(f"Original: {translation['original_text']}")
        print(f"Translated (French): {translation['translated_text']}")
        print(f"Provider: {translation['provider']}")
    except Exception as e:
        print(f"Error: {e}")
