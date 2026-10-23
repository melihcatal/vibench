import os
from deepl import Translator


def payload_translate(text, target_lang="EN"):
    api_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text


if __name__ == "__main__":
    print(payload_translate("Translate this text:...", "EN"))
