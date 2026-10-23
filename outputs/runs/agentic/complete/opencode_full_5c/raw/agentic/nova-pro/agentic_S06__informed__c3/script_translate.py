import os
from deepl import Translator

# Set up the DeepL API client
deepl_auth_key = os.getenv("DEEPL_AUTH_KEY")
translator = Translator(deepl_auth_key)


def translate_script(script, target_lang):
    return translator.translate_text(script, target_lang=target_lang)
