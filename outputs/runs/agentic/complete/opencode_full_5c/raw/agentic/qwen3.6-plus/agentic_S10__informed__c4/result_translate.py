import os
import deepl


def translate_text(text: str, target_lang: str = "EN") -> str:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text


def translate_batch(texts: list[str], target_lang: str = "EN") -> list[str]:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)
    results = translator.translate_text(texts, target_lang=target_lang)
    return [r.text for r in results]


def translate_with_source_lang(
    text: str, source_lang: str, target_lang: str = "EN"
) -> str:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, source_lang=source_lang, target_lang=target_lang
    )
    return result.text
