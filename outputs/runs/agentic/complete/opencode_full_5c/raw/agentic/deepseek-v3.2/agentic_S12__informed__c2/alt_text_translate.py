import os
import deepl
from typing import Dict, Any, List


def translate_image_descriptions(
    descriptions: List[Dict[str, Any]], target_language: str = "DE"
) -> List[Dict[str, Any]]:
    """
    Translate generated image descriptions using DeepL API.

    Args:
        descriptions: List of image description dictionaries
        target_language: Target language code (e.g., "DE" for German, "FR" for French)

    Returns:
        List of translated descriptions
    """
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

    translated_descriptions = []

    for desc in descriptions:
        original_text = desc.get("description", "")
        if not original_text:
            continue

        try:
            result = translator.translate_text(
                original_text, target_lang=target_language
            )

            translated_desc = desc.copy()
            translated_desc["translated_description"] = result.text
            translated_desc["target_language"] = target_language
            translated_desc["original_language"] = result.detected_source_lang
            translated_desc["translation_provider"] = "deepl"

            translated_descriptions.append(translated_desc)
        except Exception as e:
            print(f"DeepL translation error for description: {str(e)}")
            translated_desc = desc.copy()
            translated_desc["translated_description"] = original_text
            translated_desc["target_language"] = target_language
            translated_desc["original_language"] = "EN"
            translated_desc["translation_provider"] = "deepl-error"
            translated_desc["error"] = str(e)
            translated_descriptions.append(translated_desc)

    return translated_descriptions


def translate_single_description(
    description: str, target_language: str = "DE"
) -> Dict[str, Any]:
    """
    Translate a single image description using DeepL API.

    Args:
        description: Image description text
        target_language: Target language code

    Returns:
        Dictionary with translation results
    """
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

    try:
        result = translator.translate_text(description, target_lang=target_language)

        return {
            "original_text": description,
            "translated_text": result.text,
            "target_language": target_language,
            "source_language": result.detected_source_lang,
            "provider": "deepl",
            "success": True,
        }
    except Exception as e:
        raise Exception(f"DeepL API error: {str(e)}")
