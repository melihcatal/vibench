from speech_client import get_translation_client


def script_translate(text, target_language="es", source_language=None):
    client = get_translation_client()
    
    # Text can also be a list of strings
    result = client.translate(text, target_language=target_language, source_language=source_language)
    
    if isinstance(text, list):
        return [translation["translatedText"] for translation in result]
    else:
        return result["translatedText"]