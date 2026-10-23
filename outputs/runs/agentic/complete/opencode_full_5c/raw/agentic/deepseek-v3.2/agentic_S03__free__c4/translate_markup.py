import os
from google.cloud import translate_v2 as translate


def translate_markup(
    html_content: str, target_language: str = "es", source_language: str = "en"
) -> str:
    """Translate HTML or markup while preserving tags using Google Cloud Translation API."""
    client = translate.Client()

    result = client.translate(
        html_content,
        target_language=target_language,
        source_language=source_language,
        format_="html",
    )

    return result["translatedText"]
