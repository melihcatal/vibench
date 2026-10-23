import os
from typing import AsyncIterator, Optional

from google.cloud import translate_v2
from google.cloud.translate_v2.types import TranslateTextRequest

from speech_models import StreamingRecognitionResult


class LiveCaptionTranslator:
    def __init__(
        self,
        target_language: str = "es",
        source_language: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        self.target_language = target_language
        self.source_language = source_language
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT", "")
        self._client = translate_v2.TranslationServiceClient()
        self._parent = f"projects/{self.project_id}/locations/global"
        self._cache = {}

    def translate_text(self, text: str) -> str:
        if text in self._cache:
            return self._cache[text]

        request = TranslateTextRequest(
            contents=[text],
            target_language_code=self.target_language,
            source_language_code=self.source_language,
            parent=self._parent,
            mime_type="text/plain",
        )

        response = self._client.translate_text(request=request)
        translated = response.translations[0].translated_text
        self._cache[text] = translated
        return translated

    def translate_result(self, result: StreamingRecognitionResult) -> dict:
        translated_text = self.translate_text(result.transcript)
        return {
            "original": result.transcript,
            "translated": translated_text,
            "source_language": result.language_code,
            "target_language": self.target_language,
            "is_final": result.is_final,
            "confidence": result.confidence,
        }


async def translate_live_captions(
    caption_stream: AsyncIterator[StreamingRecognitionResult],
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> AsyncIterator[dict]:
    translator = LiveCaptionTranslator(
        target_language=target_language,
        source_language=source_language,
    )

    async for result in caption_stream:
        translated = translator.translate_result(result)
        yield translated
