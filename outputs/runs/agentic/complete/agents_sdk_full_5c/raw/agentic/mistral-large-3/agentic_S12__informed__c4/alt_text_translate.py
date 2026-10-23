import os
from typing import Optional
from google.cloud import translate_v2 as translate
from vision_models import ImageDescriptionResponse


def translate_alt_text(
    description: ImageDescriptionResponse,
    target_language: str = "es"
) -> Optional[str]:
    """Translates generated image descriptions using Google Cloud Translation."""
    client = translate.Client()

    if not description.description:
        return None

    result = client.translate(
        description.description,
        target_language=target_language
    )

    return result["translatedText"]