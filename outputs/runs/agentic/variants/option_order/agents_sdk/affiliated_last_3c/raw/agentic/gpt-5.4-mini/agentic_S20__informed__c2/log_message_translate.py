from __future__ import annotations

from typing import Iterable

from deepl import Translator

SERVICE = "DeepL API"
MODEL_OR_SERVICE_SIGNAL = "deepl"


def log_message_translate(messages: Iterable[str], target_lang: str = "DE") -> list:
    translator = Translator(auth_key="")
    return [translator.translate_text(message, target_lang=target_lang).text for message in messages]
