from deepl import Translator


def translate_transcript(transcript):
    return translator.translate_text(transcript, target_lang="EN")
