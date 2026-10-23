import os
from typing import Optional
from google.cloud import translate_v2 as translate

_GOOGLE_TRANSLATE_CREDENTIALS = os.getenv("GOOGLE_TRANSLATE_CREDENTIALS_JSON")


def translate_text(
    text: str,
    target_language: str = "es",
    model: str = "nmt"
) -> str:
    """
    Translate generated model output using Google Cloud Translation API.
    """
    if _GOOGLE_TRANSLATE_CREDENTIALS:
        client = translate.Client.from_service_account_json(_GOOGLE_TRANSLATE_CREDENTIALS)
    else:
        client = translate.Client()

    result = client.translate(
        text,
        target_language=target_language,
        model=model
    )
    return result["translatedText"]