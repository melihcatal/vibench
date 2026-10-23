from __future__ import annotations

import deepl

from vision_models import VisionDescription


class AltTextTranslator:
    def __init__(self, target_lang: str = "DE") -> None:
        self.client = deepl.Translator(auth_key=__import__("os").environ.get("DEEPL_AUTH_KEY", ""))
        self.target_lang = target_lang

    def run(self, description: VisionDescription) -> str:
        result = self.client.translate_text(description.text, target_lang=self.target_lang)
        return str(result)
