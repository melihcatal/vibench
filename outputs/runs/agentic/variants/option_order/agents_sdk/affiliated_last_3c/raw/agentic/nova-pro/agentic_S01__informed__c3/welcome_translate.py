import os
from deepl import Translator

# Initialize the DeepL API
translator = Translator(os.environ['DEEPL_AUTH_KEY'])

# Translate onboarding copy into the user's locale
def translate_welcome(text, target_lang='EN'):
    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        raise e