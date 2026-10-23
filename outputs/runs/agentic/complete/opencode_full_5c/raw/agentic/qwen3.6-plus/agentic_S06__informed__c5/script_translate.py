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
    texts: list[str], target_lang: str, source_lang: str = None
) -> list[str]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)
    kwargs = {"target_lang": target_lang.upper()}
    if source_lang:
        kwargs["source_lang"] = source_lang.upper()

    results = translator.translate_text(texts, **kwargs)
    return [r.text for r in results]


def translate_narration(script: str, target_locale: str) -> str:
    lang_map = {
        "en-US": "EN-US",
        "en-GB": "EN-GB",
        "es-ES": "ES",
        "fr-FR": "FR",
        "de-DE": "DE",
        "ja-JP": "JA",
        "zh-CN": "ZH",
        "pt-BR": "PT-BR",
        "it-IT": "IT",
        "ru-RU": "RU",
    }
    target = lang_map.get(target_locale, target_locale.split("-")[0].upper())
    return translate_script(script, target_lang=target)
