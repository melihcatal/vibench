from google.cloud import translate_v2 as translate
import os

class LiveCaptionTranslator:
    def __init__(self, target_language: str = "en"):
        self.client = translate.Client()
        self.target_language = target_language

    def translate_text(self, text: str) -> str:
        if not text.strip():
            return ""
        
        result = self.client.translate(
            text,
            target_language=self.target_language,
            source_language="auto"
        )
        return result["translatedText"]

async def translate_live_captions(caption_stream):
    translator = LiveCaptionTranslator()
    async for caption in caption_stream:
        translated = translator.translate_text(caption)
        print(f"Translated: {translated}")
        yield translated