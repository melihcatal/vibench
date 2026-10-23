import os
from google.cloud import translate_v2 as translate


def translate_image_description(description, target_language="es"):
    """Translate generated image descriptions using Google Cloud Translation."""
    client = translate.Client()

    if isinstance(description, list):
        description = " ".join(description)

    result = client.translate(description, target_language=target_language)

    return {
        "original": description,
        "translated": result["translatedText"],
        "target_language": target_language,
        "detected_language": result.get("detectedSourceLanguage", "en"),
        "provider": "Google Cloud Translation",
    }
