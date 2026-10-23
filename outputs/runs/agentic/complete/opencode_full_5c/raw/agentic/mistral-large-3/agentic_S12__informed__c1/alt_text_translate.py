import os
from typing import Optional
from deepl import Translator
from .vision_models import ImageDescriptionResponse


def alt_text_translate(
    description: ImageDescriptionResponse,
    target_lang: str = "DE",
    api_key: Optional[str] = None,
) -> str:
    """
    Translates generated image descriptions using DeepL API.
    """
    api_key = api_key or os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = Translator(auth_key=api_key)

    result = translator.translate_text(description.description, target_lang=target_lang)

    return result.text
