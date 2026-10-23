import deepl
from safety_client import get_deepl_translator
from safety_models import TranslationRequest, TranslationResponse

def appeal_translate(request: TranslationRequest) -> TranslationResponse:
    """
    Translates appeal text to a target language for review using DeepL API.

    Args:
        request: A TranslationRequest object with text and target language.

    Returns:
        A TranslationResponse object with the original and translated text.
    """
    translator = get_deepl_translator()
    
    try:
        # The DeepL Python library maps "EN-US" to the "EN" target_lang automatically
        result = translator.translate_text(
            request.text, 
            target_lang=request.target_language
        )
        
        return TranslationResponse(
            original_text=request.text,
            translated_text=result.text,
            detected_source_lang=result.detected_source_lang
        )
    except deepl.DeepLException as e:
        # Handle API errors gracefully
        raise RuntimeError(f"DeepL translation failed: {e}") from e
