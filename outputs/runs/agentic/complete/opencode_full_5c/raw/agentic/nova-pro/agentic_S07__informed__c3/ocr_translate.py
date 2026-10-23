from deepl import Translator
import os

# Set up the client
api_key = os.getenv("DEEPL_AUTH_KEY")
translator = Translator(api_key)


def translate_text(text, target_lang="EN"):
    return translator.translate_text(text, target_lang=target_lang).text
