import deepl


def compliance_note_translate(text):
    auth_key = "your_deepl_auth_key"
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang="EN-US")
    return result.text
