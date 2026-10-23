import os
from deepl import Translator

# Configuration
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

# DeepL API client
translator = Translator(DEEPL_AUTH_KEY)


def translate_text(text, target_lang):
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
