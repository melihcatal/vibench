from google.cloud import translate_v2 as translate
from typing import Generator, Dict, Any
import asyncio


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es", source_language: str = "en"):
        self.translate_client = translate.Client()
        self.target_language = target_language
        self.source_language = source_language

    def translate_text(self, text: str) -> Dict[str, Any]:
        try:
            result = self.translate_client.translate(
                text,
                target_language=self.target_language,
                source_language=self.source_language,
                model="nmt",
            )

            return {
                "original_text": text,
                "translated_text": result["translatedText"],
                "detected_language": result.get(
                    "detectedSourceLanguage", self.source_language
                ),
                "target_language": self.target_language,
            }
        except Exception as e:
            return {
                "original_text": text,
                "translated_text": text,
                "error": str(e),
                "target_language": self.target_language,
            }

    def translate_caption_stream(
        self, caption_stream: Generator[Dict[str, Any], None, None]
    ) -> Generator[Dict[str, Any], None, None]:
        for caption in caption_stream:
            if caption.get("is_final", False):
                transcript = caption.get("transcript", "")

                if transcript.strip():
                    translation = self.translate_text(transcript)

                    yield {
                        **caption,
                        "translation": translation,
                        "original_language": self.source_language,
                        "target_language": self.target_language,
                    }
                else:
                    yield caption
            else:
                yield caption


class AsyncCaptionTranslator:
    def __init__(self, target_language: str = "es"):
        self.translate_client = translate.Client()
        self.target_language = target_language

    async def translate_async(
        self, text: str, source_language: str = "en"
    ) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()

        try:
            result = await loop.run_in_executor(
                None,
                lambda: self.translate_client.translate(
                    text,
                    target_language=self.target_language,
                    source_language=source_language,
                    model="nmt",
                ),
            )

            return {
                "original_text": text,
                "translated_text": result["translatedText"],
                "detected_language": result.get(
                    "detectedSourceLanguage", source_language
                ),
                "target_language": self.target_language,
            }
        except Exception as e:
            return {
                "original_text": text,
                "translated_text": text,
                "error": str(e),
                "target_language": self.target_language,
            }

    async def process_caption_stream(self, caption_stream):
        async for caption in caption_stream:
            if caption.get("is_final", False):
                transcript = caption.get("transcript", "")

                if transcript.strip():
                    translation = await self.translate_async(transcript)

                    yield {
                        **caption,
                        "translation": translation,
                        "target_language": self.target_language,
                    }
                else:
                    yield caption
            else:
                yield caption


def translate_live_captions(caption_stream, target_language="fr"):
    translator = LiveCaptionTranslator(target_language=target_language)

    for translated_caption in translator.translate_caption_stream(caption_stream):
        if "translation" in translated_caption:
            trans = translated_caption["translation"]
            print(f"Original: {trans['original_text']}")
            print(f"Translated ({target_language}): {trans['translated_text']}")
            print("-" * 50)

        yield translated_caption


if __name__ == "__main__":
    test_captions = [
        {"transcript": "Hello world", "is_final": True},
        {"transcript": "This is a test", "is_final": True},
        {"transcript": "Partial result", "is_final": False},
    ]

    for result in translate_live_captions(test_captions, "es"):
        print(result)
