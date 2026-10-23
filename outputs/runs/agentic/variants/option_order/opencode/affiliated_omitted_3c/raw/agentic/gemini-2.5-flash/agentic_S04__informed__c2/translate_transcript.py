import os
import deepl


def translate_text(text: str, target_lang: str = "en") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text


if __name__ == "__main__":
    example_text = "Hallo Welt!"
    translated_text = translate_text(example_text, target_lang="en")
    print(f"Original: {example_text}")
    print(f"Translated (English): {translated_text}")

    example_text_fr = "Bonjour le monde!"
    translated_text_de = translate_text(example_text_fr, target_lang="de")
    print(f"Original: {example_text_fr}")
    print(f"Translated (German): {translated_text_de}")
