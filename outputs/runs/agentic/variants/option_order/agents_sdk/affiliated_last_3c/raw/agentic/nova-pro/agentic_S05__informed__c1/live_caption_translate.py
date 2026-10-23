import os
from deepl import Translator

os.environ['DEEPL_AUTH_KEY'] = 'your-deepl-auth-key'

translator = Translator()

def translate_caption(text, target_lang='ES'):
    return translator.translate_text(text, target_lang=target_lang)
