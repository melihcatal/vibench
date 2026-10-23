import os
import deepl


def translate_description(description, target_lang="EN"):
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(description, target_lang=target_lang)
    return result.text


if __name__ == "__main__":
    description = "Example description to translate."
    translated_description = translate_description(description)
    print("Translated Description:", translated_description)
