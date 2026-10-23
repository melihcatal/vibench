import os
from deepl import Translator

def stored_text_translate(text, target_lang='EN'):
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    print(result.text)
    return result.text

if __name__ == '__main__':\n    stored_text_translate('Hello, world!')