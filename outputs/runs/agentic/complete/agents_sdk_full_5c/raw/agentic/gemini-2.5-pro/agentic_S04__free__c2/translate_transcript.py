from speech_client import deepl_client
from speech_models import TranslationRequest, TranslationResponse

def translate_text_deepl(request: TranslationRequest) -> TranslationResponse:
    """
    Translates a text segment using the DeepL API.

    Args:
        request: A TranslationRequest object containing the text and target language.

    Returns:
        A TranslationResponse object with original, translated, and source language.
    """
    result = deepl_client.translate_text(
        request.text,
        target_lang=request.target_language
    )
    
    return TranslationResponse(
        original_text=request.text,
        translated_text=result.text,
        detected_source_language=result.detected_source_lang
    )
