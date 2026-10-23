import os
from typing import Optional, List
import deepl


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def translate_alt_text(
    text: str,
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
) -> str:
    if not text.strip():
        return ""
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    kwargs = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang
    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_alt_text_batch(
    texts: List[str],
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
) -> List[str]:
    if not texts:
        return []
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    kwargs = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang
    results = translator.translate_text(texts, **kwargs)
    return [r.text for r in results]


if __name__ == "__main__":
    sample = "A photo of a mountain landscape with a lake in the foreground."
    translated = translate_alt_text(sample, target_lang="ES")
    print(translated)
