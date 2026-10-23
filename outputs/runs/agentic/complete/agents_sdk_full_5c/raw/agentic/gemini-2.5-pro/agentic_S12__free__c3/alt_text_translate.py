import deepl
from vision_client import get_deepl_api_key
from vision_models import Translation

def translate_text(text: str, target_lang: str = "DE") -> Translation:
    """
    Translates text to a target language using the DeepL API.
    
    :param text: The text to translate.
    :param target_lang: The target language code (e.g., "DE" for German, "FR" for French).
    :return: A Translation object.
    """
    auth_key = get_deepl_api_key()
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
        
    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(text, target_lang=target_lang)
    
    return Translation(
        source_text=text,
        translated_text=result.text,
        target_language=result.detected_source_lang
    )
