import os
from deepl import Translator

def translate_caption(text, target_lang):
    os.environ["DEEPL_AUTH_KEY"] = "your-deepl-auth-key"
    translator = Translator()
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text