import os
from deepl import Translator

DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

def translate_result(text: str, target_lang: str = 'EN-US') -> str:
    \"\"\"Translate generated model output using DeepL.\"\"
    translator = Translator(DEEPL_API_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result.text)
