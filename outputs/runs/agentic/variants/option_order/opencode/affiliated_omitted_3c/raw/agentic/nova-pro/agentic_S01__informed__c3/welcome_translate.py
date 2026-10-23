import os
from deepl import Translator

os.environ["DEEPL_AUTH_KEY"] = "your-deepl-auth-key"


def translate_text(text, target_lang="EN"):
    translator = Translator()
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
