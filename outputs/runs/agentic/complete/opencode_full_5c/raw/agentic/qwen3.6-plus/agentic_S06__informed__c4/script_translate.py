import os
import deepl


def translate_script(text: str, target_lang: str, source_lang: str = None) -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    kwargs = {"target_lang": target_lang.upper()}
    if source_lang:
        kwargs["source_lang"] = source_lang.upper()
    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_script_batch(
    texts: list, target_lang: str, source_lang: str = None
) -> list:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    kwargs = {"target_lang": target_lang.upper()}
    if source_lang:
        kwargs["source_lang"] = source_lang.upper()
    results = translator.translate_text(texts, **kwargs)
    return [r.text for r in results]
