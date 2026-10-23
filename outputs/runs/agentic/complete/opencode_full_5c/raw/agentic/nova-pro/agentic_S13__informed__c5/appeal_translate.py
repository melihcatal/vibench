import os
from deepl import Translator

# Set up the DeepL client
translator = Translator(os.getenv("DEEPL_AUTH_KEY"))


def appeal_translate(text, target_lang="EN"):
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
