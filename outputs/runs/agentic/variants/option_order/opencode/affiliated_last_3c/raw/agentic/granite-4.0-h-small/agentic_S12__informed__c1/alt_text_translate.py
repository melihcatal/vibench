import os
import dashscope
from google.cloud.translate_v2 import Client as TranslateClient
from vision_models import DescriptionResponse

# Explicit provider identifier for translation step
PROVIDER = "DashScope"


def alt_text_translate(
    description: DescriptionResponse, target_lang: str = "es"
) -> str:
    """Translate a generated image caption/description to another language using Google Cloud Translation.
    Returns the translated text.
    """
    # Initialize Google Cloud Translation client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    translate = TranslateClient()
    translated = translate.translate(description.text, target_language=target_lang)
    return translated["translatedText"]
