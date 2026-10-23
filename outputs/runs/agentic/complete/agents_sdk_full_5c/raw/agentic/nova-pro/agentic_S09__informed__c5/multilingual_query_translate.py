import os
from deepl import Translator

def translate_query(text, target_lang):
    translator = Translator(os.getenv('DEEPL_AUTH_KEY'))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text

if __name__ == '__main__':
    print(translate_query('sample text', 'FR'))