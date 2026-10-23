from deepl import Translator


def translate_transcript(transcript):
    translator = Translator("DEEPL_AUTH_KEY")
    result = translator.translate_text(transcript, target_lang="EN-US")
    return result.text
