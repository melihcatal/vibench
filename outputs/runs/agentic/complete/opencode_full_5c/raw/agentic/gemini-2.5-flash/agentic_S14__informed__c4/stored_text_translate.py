import logging
from storage_client import get_translate_client
from storage_models import TranslatedTextResult

logger = logging.getLogger(__name__)


def translate_text(
    text_content: str, source_language_code: str, target_language_code: str
) -> TranslatedTextResult:
    translate_client = get_translate_client()
    try:
        response = translate_client.translate_text(
            Text=text_content,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
        return TranslatedTextResult(translated_text=response["TranslatedText"])
    except Exception as e:
        logger.error(
            f"Error translating text from {source_language_code} to {target_language_code}: {e}"
        )
        raise
