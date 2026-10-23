from google.cloud import translate_v2 as translate
from vision_models import ImageDescription
import os

def translate_image_description(description: ImageDescription, target_language: str = "es") -> ImageDescription:
    """Translates a generated image description using Google Cloud Translation."""
    translate_client = translate.Client()

    result = translate_client.translate(
        description.description,
        target_language=target_language
    )

    translated_text = result['translatedText']
    return ImageDescription(description=translated_text)
