import os
import deepl


def translate_query(query: str, target_lang: str = "en") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set.")

    translator = deepl.Translator(auth_key)  # DeepL specific client

    result = translator.translate_text(query, target_lang=target_lang)
    return result.text


if __name__ == "__main__":
    os.environ["DEEPL_AUTH_KEY"] = "YOUR_DEEPL_AUTH_KEY"  # Placeholder for actual key

    german_query = "Wie geht es Ihnen?"
    english_translation = translate_query(german_query, target_lang="en")
    # print(f"Original German query: '{german_query}'")
    # print(f"Translated English query: '{english_translation}'")

    spanish_query = "¿Qué tal?"
    english_translation_2 = translate_query(spanish_query, target_lang="en")
    # print(f"Original Spanish query: '{spanish_query}'")
    # print(f"Translated English query: '{english_translation_2}'")
