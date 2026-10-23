import deepl
from vision_models import ImageDescriptionResponse
import os

def translate_alt_text(description: str, target_lang: str = "DE") -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(description, target_lang=target_lang)
    return result.text