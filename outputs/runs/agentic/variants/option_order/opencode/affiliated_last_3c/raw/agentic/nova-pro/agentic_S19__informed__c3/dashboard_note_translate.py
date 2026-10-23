import os
from deepl import Translator

# Set up client
translator = Translator(os.getenv("DEEPL_AUTH_KEY"))


# Function to translate text
def translate_text(text, target_lang):
    return translator.translate_text(text, target_lang=target_lang)
