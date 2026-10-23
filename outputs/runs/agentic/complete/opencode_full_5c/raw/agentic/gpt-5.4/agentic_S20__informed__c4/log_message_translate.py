from __future__ import annotations

import deepl


def log_message_translate(
    text: str, target_lang: str, source_lang: str | None = None
) -> str:
    translator = deepl.Translator(auth_key=__import__("os").environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return result.text
