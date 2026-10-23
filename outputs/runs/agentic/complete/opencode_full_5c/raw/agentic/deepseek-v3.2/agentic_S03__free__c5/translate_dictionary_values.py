import os
from translation_client import get_translation_client


def translate_dictionary_values(
    data_dict, source_lang="en", target_lang="es", keys_to_translate=None
):
    """
    Translate dictionary values while preserving keys using Google Cloud Translation API.

    Args:
        data_dict: Dictionary with string values to translate
        source_lang: Source language code (default: "en")
        target_lang: Target language code (default: "es")
        keys_to_translate: Optional list of keys to translate (default: all string values)

    Returns:
        Dictionary with same keys but translated values
    """
    client = get_translation_client()

    try:
        from google.cloud import translate_v2 as translate

        result_dict = {}

        # Determine which keys to process
        keys = keys_to_translate if keys_to_translate else data_dict.keys()

        for key in keys:
            if key not in data_dict:
                continue

            value = data_dict[key]

            # Only translate string values
            if isinstance(value, str) and value.strip():
                translation_result = client.translate(
                    value, source_language=source_lang, target_language=target_lang
                )
                result_dict[key] = translation_result["translatedText"]
            else:
                # Keep non-string or empty values as-is
                result_dict[key] = value

        return result_dict

    except Exception as e:
        raise Exception(f"Dictionary translation failed: {str(e)}")
