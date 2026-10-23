from typing import Optional

from google.cloud import translate_v2 as translate
from botocore.exceptions import ClientError


def translate_stored_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
) -> str:
    """
    Translates text extracted from a stored document using Google Cloud Translation API.

    Args:
        text: Text to translate.
        target_language: Target language code (e.g., "es", "fr").
        source_language: Optional source language code (e.g., "en").

    Returns:
        Translated text.

    Raises:
        ClientError: If the translation fails.
    """
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language,
        )

        return result["translatedText"]
    except Exception as e:
        raise ClientError(
            error_response={"Error": {"Code": "TRANSLATION_FAILED", "Message": str(e)}},
            operation_name="translate_stored_text",
        )
