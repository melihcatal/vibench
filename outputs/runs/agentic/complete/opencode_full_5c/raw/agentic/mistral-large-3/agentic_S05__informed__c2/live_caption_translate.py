import os
from deepl import Translator

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


class LiveCaptionTranslator:
    def __init__(self, target_lang: str = "ES"):
        self.translator = Translator(DEEPL_AUTH_KEY)
        self.target_lang = target_lang

    async def translate_text(self, text: str) -> str:
        result = self.translator.translate_text(text, target_lang=self.target_lang)
        return result.text


async def translate_live_captions(caption_stream, target_lang: str = "ES"):
    translator = LiveCaptionTranslator(target_lang)
    async for caption in caption_stream:
        translated_text = await translator.translate_text(caption.get("text", ""))
        yield {
            "original_text": caption.get("text", ""),
            "translated_text": translated_text,
            "type": caption.get("type", "interim"),
        }
