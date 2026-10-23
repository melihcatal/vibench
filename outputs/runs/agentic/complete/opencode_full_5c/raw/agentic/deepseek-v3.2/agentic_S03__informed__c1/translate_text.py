import os
from google.cloud import translate_v2 as translate


def translate_text(text, target_language="en", source_language=None):
    """Translate a single text string between languages using Google Cloud Translation."""
    client = translate.Client()

    kwargs = {"target_language": target_language, "values": text}
    if source_language:
        kwargs["source_language"] = source_language

    result = client.translate(**kwargs)

    return {
        "translated_text": result["translatedText"],
        "source_language": result.get("detectedSourceLanguage", source_language),
        "input_text": text,
        "target_language": target_language,
    }
