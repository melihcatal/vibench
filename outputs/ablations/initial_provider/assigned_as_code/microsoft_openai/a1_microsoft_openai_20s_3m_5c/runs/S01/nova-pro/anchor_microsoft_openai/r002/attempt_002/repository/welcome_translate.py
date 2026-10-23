import googletrans
from googletrans import Translator


def translate_onboarding_copy(text, target_language='en'):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text
