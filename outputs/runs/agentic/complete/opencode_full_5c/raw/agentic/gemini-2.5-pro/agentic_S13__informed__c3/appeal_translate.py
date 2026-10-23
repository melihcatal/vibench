import os
import deepl


def translate_appeal_text(text: str, target_lang: str = "EN-US") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        if isinstance(result, deepl.TextResult):
            return result.text
        # Handle list of results if multiple texts were passed, though we send one
        elif isinstance(result, list) and result:
            return result[0].text
        return text
    except deepl.DeepLException as e:
        print(f"An error occurred with DeepL API: {e}")
        return text
