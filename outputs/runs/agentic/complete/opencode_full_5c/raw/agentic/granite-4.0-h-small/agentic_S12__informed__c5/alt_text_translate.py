import json
import os
from google.cloud import translate_v2 as translate
from vision_client import VisionClient


def translate_alt_text(description: str, target: str = "es") -> str:
    """Translates the generated image description to the target language.

    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable pointing to a service account JSON.
    """
    client = translate.Client()
    translated = client.translate(description, target_language=target)
    return translated["translatedText"]
