from google.cloud import translate_v2 as translate
from vision_models import ImageDescription
import os


def alt_text_translate(description: ImageDescription, target_language: str) -> str:
    """
    Translates the image description text to a target language.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    translate_client = translate.Client()

    if not description or not description.text:
        return ""

    result = translate_client.translate(
        description.text, target_language=target_language
    )
    return result["translatedText"]
