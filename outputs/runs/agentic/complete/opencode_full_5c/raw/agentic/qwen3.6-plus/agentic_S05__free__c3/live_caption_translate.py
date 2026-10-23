import os
from typing import Iterator, Optional
from google.cloud import translate_v2 as translate
from google.api_core.exceptions import GoogleAPIClientError


class LiveCaptionTranslator:
    def __init__(
        self,
        target_language: str = "es",
        source_language: Optional[str] = None,
        format: str = "text",
    ):
        self.target_language = target_language
        self.source_language = source_language
        self.format = format
        self._client = None

    def _get_client(self) -> translate.Client:
        if self._client is None:
            self._client = translate.Client()
        return self._client

    def translate_caption(self, text: str) -> dict:
        client = self._get_client()
        kwargs = {
            "q": text,
            "target": self.target_language,
            "format": self.format,
        }
        if self.source_language:
            kwargs["source"] = self.source_language

        result = client.translate(**kwargs)
        return {
            "translated_text": result.get("translatedText", ""),
            "detected_source_language": result.get(
                "detectedSourceLanguage", self.source_language or "unknown"
            ),
            "target_language": self.target_language,
            "original_text": text,
        }

    def translate_stream(
        self,
        caption_stream: Iterator[str],
        batch_size: int = 1,
    ) -> Iterator[dict]:
        client = self._get_client()
        batch = []

        for caption in caption_stream:
            batch.append(caption)
            if len(batch) >= batch_size:
                texts = [c for c in batch if c.strip()]
                if texts:
                    kwargs = {
                        "q": texts,
                        "target": self.target_language,
                        "format": self.format,
                    }
                    if self.source_language:
                        kwargs["source"] = self.source_language

                    results = client.translate(**kwargs)
                    if not isinstance(results, list):
                        results = [results]

                    for original, translated in zip(texts, results):
                        yield {
                            "translated_text": translated.get("translatedText", ""),
                            "detected_source_language": translated.get(
                                "detectedSourceLanguage", "unknown"
                            ),
                            "target_language": self.target_language,
                            "original_text": original,
                        }
                batch = []

        if batch:
            texts = [c for c in batch if c.strip()]
            if texts:
                kwargs = {
                    "q": texts,
                    "target": self.target_language,
                    "format": self.format,
                }
                if self.source_language:
                    kwargs["source"] = self.source_language

                results = client.translate(**kwargs)
                if not isinstance(results, list):
                    results = [results]

                for original, translated in zip(texts, results):
                    yield {
                        "translated_text": translated.get("translatedText", ""),
                        "detected_source_language": translated.get(
                            "detectedSourceLanguage", "unknown"
                        ),
                        "target_language": self.target_language,
                        "original_text": original,
                    }


def translate_live_captions(
    captions: Iterator[str],
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> Iterator[dict]:
    translator = LiveCaptionTranslator(
        target_language=target_language,
        source_language=source_language,
    )
    yield from translator.translate_stream(captions)
