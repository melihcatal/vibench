from translation_client import TranslationClient
from translation_models import *


def translate_text(
    source_text: str,
    src_lang: str = GOOGLE_SOURCE_LANG,
    tgt_lang: str = GOOGLE_TARGET_LANG,
) -> str:
    """
    Translates a single text string between languages using the configured provider.

    Args:
        source_text: The text to translate.
        src_lang: Source language code (default from model config).
        tgt_lang: Target language code (default from model config).

    Returns:
        Translated text string.
    """
    client = TranslationClient.get()
    if isinstance(client, object) and hasattr(client, "translate"):
        # Google Cloud Translation SDK style
        result = client.translate(
            source_text, source_language=src_lang, target_language=tgt_lang
        )
        return result["translatedText"]
    elif isinstance(client, dict) and "translateText" in client:
        # Amazon Translate style response shape
        result = client.translate_text(
            Text=source_text, SourceLanguageCode=src_lang, TargetLanguageCode=tgt_lang
        )
        return result["TranslatedText"]
    else:
        raise NotImplementedError("Unsupported translation client or response format")
