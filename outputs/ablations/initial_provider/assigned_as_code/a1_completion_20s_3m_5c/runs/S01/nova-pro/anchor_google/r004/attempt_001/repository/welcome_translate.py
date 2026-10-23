import googletrans
from googletrans import Translator


def welcome_translate(text, locale):
    translator = Translator()
    translated = translator.translate(text, dest=locale)
    return translated.text