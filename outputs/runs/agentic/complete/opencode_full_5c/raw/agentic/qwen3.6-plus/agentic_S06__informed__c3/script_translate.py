from typing import List, Optional
import deepl

DEEPL_AUTH_KEY = ""


def get_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    key = auth_key or DEEPL_AUTH_KEY
    return deepl.Translator(key)


def translate_script(
    text: str,
    source_lang: str = "",
    target_lang: str = "EN-US",
    auth_key: Optional[str] = None,
    preserve_formatting: bool = True,
    formality: Optional[str] = None,
) -> str:
    translator = get_translator(auth_key)
    kwargs = {
        "source_lang": source_lang if source_lang else None,
        "target_lang": target_lang,
        "preserve_formatting": preserve_formatting,
    }
    if formality:
        kwargs["formality"] = formality
    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_script_batch(
    texts: List[str],
    source_lang: str = "",
    target_lang: str = "EN-US",
    auth_key: Optional[str] = None,
    preserve_formatting: bool = True,
    formality: Optional[str] = None,
) -> List[str]:
    translator = get_translator(auth_key)
    kwargs = {
        "source_lang": source_lang if source_lang else None,
        "target_lang": target_lang,
        "preserve_formatting": preserve_formatting,
    }
    if formality:
        kwargs["formality"] = formality
    results = translator.translate_text(texts, **kwargs)
    return [r.text for r in results]
