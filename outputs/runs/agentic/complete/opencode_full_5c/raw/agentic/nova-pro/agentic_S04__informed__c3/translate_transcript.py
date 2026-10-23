import deepl


def translate_transcript(text):
    client = deepl.Client("DEEPL_AUTH_KEY")
    result = client.translate_text(text, target_lang="EN-US")
    return result.text
