import os
from deepl import Translator
from typing import Optional


def get_translator() -> Translator:
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    return Translator(api_key)


def translate_text_with_client(
    translator: Translator,
    text: str,
    source_lang: Optional[str] = None,
    target_lang: str = "EN",
    tag_handling: Optional[str] = None,
) -> str:
    kwargs = {
        "source_lang": source_lang,
        "target_lang": target_lang,
    }
    if tag_handling:
        kwargs["tag_handling"] = tag_handling
    result = translator.translate_text(text, **kwargs)
    return result.text
