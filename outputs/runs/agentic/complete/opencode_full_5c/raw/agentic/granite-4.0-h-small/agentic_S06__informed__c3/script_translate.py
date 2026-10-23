import os
import deepl

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def translate_text(text: str, target_lang: str = "FR") -> str:
    """Translate source text to target language using DeepL API.

    Args:
        text (str): The source narrative text.
        target_lang (str): ISO language code for target (default 'FR').

    Returns:
        str: Translated text.
    """
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.raw_text


# Example invocation (commented out)
# translated = translate_text('Hello, how are you?')
# print(translated)
