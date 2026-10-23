from vision_client import get_deepl_translator
from vision_models import ImageDescription, TranslatedText

def translate_description(description: ImageDescription, target_lang: str = "DE") -> TranslatedText:
    """
    Translates an image description to a target language using the DeepL API.

    Args:
        description: The ImageDescription object to translate.
        target_lang: The target language code (e.g., 'DE' for German).

    Returns:
        A TranslatedText object with the original and translated text.
    """
    translator = get_deepl_translator()
    original_text = description.description

    result = translator.translate_text(original_text, target_lang=target_lang)
    
    return TranslatedText(
        original_text=original_text,
        translated_text=result.text,
        target_language=target_lang
    )
