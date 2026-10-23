import deepl


def translate_payload_text(text, target_lang="ES"):
    translator = deepl.Translator(__import__("os").environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang)
    return {"translated_text": result.text, "target_lang": target_lang}
