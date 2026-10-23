import googletrans
from googletrans import Translator


def translate_result(payload, target_language='en'):
    translator = Translator()
    translation = translator.translate(payload["text"], dest=target_language)
    return {"text": translation.text}