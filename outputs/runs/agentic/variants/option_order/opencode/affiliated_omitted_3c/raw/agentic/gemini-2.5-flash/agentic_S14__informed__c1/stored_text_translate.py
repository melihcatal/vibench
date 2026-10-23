import logging
from storage_client import TranslateClient
from storage_models import TextTranslateRequest, TextTranslateResponse

logger = logging.getLogger(__name__)


def translate_text_content(request: TextTranslateRequest) -> TextTranslateResponse:
    """Translates text using Amazon Translate."""
    translate_client = TranslateClient().get_client()

    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code,
        )
        translated_text = response.get("TranslatedText", "")
        logger.info(
            f"Successfully translated text from {request.source_language_code} to {request.target_language_code} using Amazon Translate."
        )
        return TextTranslateResponse(translated_text=translated_text)
    except Exception as e:
        logger.error(f"Error translating text with Amazon Translate: {e}")
        raise
