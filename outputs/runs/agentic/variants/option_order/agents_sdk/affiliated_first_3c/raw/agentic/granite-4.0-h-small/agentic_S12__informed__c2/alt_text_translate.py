# alt_text_translate.py
import os
from deepl import DeepL
from vision_models import ImageDescriptionResponse

def translate_alt_text(description: ImageDescriptionResponse, target_lang='es') -> List[str]:
    translator = DeepL(auth_key=os.getenv('DEEPL_AUTH_KEY'))
    # Use the first description text as the source alt text
    source_text = description.descriptions[0]['text'] if description.descriptions else ''
    if not source_text:
        return []
    translation = translator.translate_text(source_text, target_lang=target_lang)
    return [translation['text']]
