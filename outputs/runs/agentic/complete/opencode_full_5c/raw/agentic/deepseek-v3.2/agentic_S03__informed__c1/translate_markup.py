import os
from google.cloud import translate_v2 as translate
import re


def translate_markup(html_content, target_language="en", source_language=None):
    """Translate HTML or markup while preserving tags using Google Cloud Translation."""
    client = translate.Client()

    kwargs = {
        "target_language": target_language,
        "values": html_content,
        "format_": "html",
    }
    if source_language:
        kwargs["source_language"] = source_language

    result = client.translate(**kwargs)

    return {
        "translated_html": result["translatedText"],
        "source_language": result.get("detectedSourceLanguage", source_language),
        "target_language": target_language,
        "format": "html",
    }
