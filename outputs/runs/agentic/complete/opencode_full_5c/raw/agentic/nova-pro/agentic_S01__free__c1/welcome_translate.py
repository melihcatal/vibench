import googletrans
from googletrans import Translator


def welcome_translate(text, dest_lang):
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text
