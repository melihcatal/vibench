import os
import deepl
from vision_models import ImageDescription

translator = deepl.Translator(os.getenv('DEEPL_AUTH_KEY'))

def alt_text_translate(description: ImageDescription, target_lang: str = 'es') -> ImageDescription:
    result = translator.translate_text(description['description'], target_lang=target_lang)
    return {'description': result.text}