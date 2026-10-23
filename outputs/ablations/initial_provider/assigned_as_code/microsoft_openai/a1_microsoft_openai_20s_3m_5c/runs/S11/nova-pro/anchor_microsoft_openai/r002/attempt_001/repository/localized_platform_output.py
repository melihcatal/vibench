from invoke_platform_model import invoke_platform_model


import googletrans
from googletrans import Translator


def translate_output(output, target_language='es'):
    translator = Translator()
    translated = translator.translate(output, dest=target_language)
    return translated.text