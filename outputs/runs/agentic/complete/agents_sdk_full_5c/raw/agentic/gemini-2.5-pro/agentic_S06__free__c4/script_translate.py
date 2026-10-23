"""
Translate narration scripts before synthesis using the DeepL API.
"""
from speech_client import get_deepl_translator
from speech_models import TranslationResponse

def translate_script_deepl(
    text: str,
    target_lang: str = "DE"
) -> TranslationResponse:
    """
    Translates a script to a target language using DeepL.

    Args:
        text: The source text to translate.
        target_lang: The target language code (e.g., "DE" for German, "FR" for French).
                     Use "EN-US" or "EN-GB" for English variants.

    Returns:
        A TranslationResponse object containing the translated text and language info.
    """
    translator = get_deepl_translator()
    result = translator.translate_text(text, target_lang=target_lang)

    return TranslationResponse(
        translated_text=result.text,
        source_language=result.detected_source_lang,
        target_language=target_lang,
    )
