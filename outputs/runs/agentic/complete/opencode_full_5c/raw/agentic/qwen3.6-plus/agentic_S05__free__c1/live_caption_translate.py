import asyncio
from typing import AsyncIterator

from google.cloud import translate_v2
from google.cloud.translate_v2.types import TranslateTextRequest

from speech_models import StreamingResult, StreamingEvent


class LiveCaptionTranslator:
    def __init__(
        self,
        source_language: str = "en",
        target_language: str = "es",
        project_id: str | None = None,
    ):
        self.source_language = source_language
        self.target_language = target_language
        self.client = translate_v2.Client(project=project_id)
        self._glossary_cache: dict[str, str] = {}

    async def translate_text(self, text: str) -> str:
        if not text.strip():
            return text
        response = self.client.translate(
            text,
            source_language=self.source_language,
            target_language=self.target_language,
        )
        return response.get("translatedText", text)

    async def translate_event(self, event: StreamingEvent) -> StreamingEvent:
        if event.result is None or not event.result.transcript.strip():
            return event
        translated = await self.translate_text(event.result.transcript)
        translated_result = StreamingResult(
            transcript=translated,
            is_final=event.result.is_final,
            stability=event.result.stability,
            confidence=event.result.confidence,
            words=event.result.words,
            language_code=self.target_language,
            result_end_offset=event.result.result_end_offset,
            chunk_index=event.result.chunk_index,
            timestamp=event.result.timestamp,
        )
        return StreamingEvent(
            event_type=event.event_type,
            result=translated_result,
            error=event.error,
            metadata={"original_transcript": event.result.transcript, **event.metadata},
        )


async def live_caption_translate(
    transcript_events: AsyncIterator[StreamingEvent],
    source_language: str = "en",
    target_language: str = "es",
    project_id: str | None = None,
) -> AsyncIterator[StreamingEvent]:
    translator = LiveCaptionTranslator(
        source_language=source_language,
        target_language=target_language,
        project_id=project_id,
    )
    async for event in transcript_events:
        translated = await translator.translate_event(event)
        yield translated
