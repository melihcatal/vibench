import os
import deepl
from typing import Optional


def get_deepl_translator() -> deepl.Translator:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    return deepl.Translator(auth_key)


def translate_appeal(
    appeal_text: str,
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> str:
    if translator is None:
        translator = get_deepl_translator()

    source_lang_param = source_language if source_language else None

    result = translator.translate_text(
        appeal_text,
        source_lang=source_lang_param,
        target_lang=target_language,
        formality="less",
        context="This is an appeal text for a content moderation decision review.",
    )

    return result.text


def translate_appeal_batch(
    appeal_texts: list[str],
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> list[str]:
    if translator is None:
        translator = get_deepl_translator()

    source_lang_param = source_language if source_language else None

    results = translator.translate_text(
        appeal_texts,
        source_lang=source_lang_param,
        target_lang=target_language,
        formality="less",
        context="These are appeal texts for content moderation decision reviews.",
    )

    return [r.text for r in results]


if __name__ == "__main__":
    import sys

    text = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "I disagree with this decision. Please review my case."
    )
    translated = translate_appeal(text, target_language="DE")
    print(f"Original: {text}")
    print(f"Translated: {translated}")
