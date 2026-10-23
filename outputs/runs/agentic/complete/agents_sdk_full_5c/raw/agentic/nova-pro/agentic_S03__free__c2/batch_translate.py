import os
from deepl import Translator

def batch_translate(texts, target_lang='EN'):
    auth_key = os.getenv('DEEPL_API_KEY')
    translator = Translator(auth_key)
    results = [translator.translate_text(text, target_lang=target_lang).text for text in texts]
    return results