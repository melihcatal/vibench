import googletrans
from googletrans import Translator

def translate_onboarding_copy(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text