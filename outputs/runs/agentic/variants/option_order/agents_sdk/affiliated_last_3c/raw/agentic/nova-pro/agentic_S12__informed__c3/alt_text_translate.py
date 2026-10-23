import os
from deepl import Translator

os.environ["DEEPL_AUTH_KEY"] = "your-deepl-auth-key"

translator = Translator(os.getenv('DEEPL_AUTH_KEY'))

def translate_description(description, target_lang='EN'):
    result = translator.translate_text(description, target_lang=target_lang)
    return result.text