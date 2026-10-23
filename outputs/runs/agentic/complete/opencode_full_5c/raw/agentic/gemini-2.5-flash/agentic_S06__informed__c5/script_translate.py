import os
from google.cloud import translate_v2 as translate


def translate_script(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Translates a narration script using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set,
    or configured service account for authentication.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]
