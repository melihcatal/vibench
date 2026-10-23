from __future__ import annotations

import os
from typing import List

from deepgram import DeepgramClient
from deepl import DeepLClient

from speech_models import normalize_text


class LiveCaptionTranslator:
    def __init__(self) -> None:
        self.translation_client = DeepLClient(os.environ["DEEPL_AUTH_KEY"])
        self.target_lang = os.getenv("DEEPL_TARGET_LANG", "DE")

    def translate_caption(self, caption: str) -> str:
        caption = normalize_text(caption)
        result = self.translation_client.translate_text(caption, target_lang=self.target_lang)
        return result.text

    def translate_many(self, captions: List[str]) -> List[str]:
        return [self.translate_caption(c) for c in captions]
