import os
from deepl import Translator


def translate_transcript(transcript):
    translator = Translator(os.environ["DEEPL_AUTH_KEY"])
    translated_text = translator.translate_text(transcript, target_lang="EN-US")
    return translated_text.text
