import os
from vision_client import ImageVisionClient
from vision_models import DescriptionResult
from google.cloud import translate_v2 as translate

def alt_text_translate(alt_text: str, target_lang: str = "es") -> str:
    """Translate generated image description (alt text) to a target language using Google Cloud Translation."""
    client = translate.Client()
    response = client.translate(alt_text, target_language=target_lang)
    return response["translatedText"]
