from __future__ import annotations

import os
from typing import List

from deep_translator import DeepLTranslator


def log_message_translate(text: str, target_language: str) -> str:
    api_key = os.environ["DEEPL_AUTH_KEY"]
    translator = DeepLTranslator(api_key=api_key, source="auto", target=target_language)
    return translator.translate(text)
