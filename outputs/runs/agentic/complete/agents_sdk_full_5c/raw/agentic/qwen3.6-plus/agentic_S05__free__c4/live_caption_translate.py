"""Translate live captions into another language using Google Cloud Translation API."""

from typing import AsyncGenerator, List, Optional

from google.cloud import translate_v2 as translate

from speech_models import TranscriptSegment, StreamingSpeechEvent


class LiveCaptionTranslator:
    """Translates live caption segments using Google Cloud Translation API v2.

    Uses google.cloud.translate_v2.TranslationClient to detect language and
    translate transcript segments from a live streaming Speech-to-Text session.
    """

    def __init__(
        self,
        target_language: str = "es",
        source_language: Optional[str] = None,
        format: str = "text",
    ):
        """Initialize the Google Cloud Translation client.

        Args:
            target_language: ISO 639-1 language code for translation target (e.g., "es", "fr").
            source_language: Source language code, or None for auto-detect by Google Cloud.
            format: Input format ("text" or "html").
        """
        self.target_language = target_language
        self.source_language = source_language
        self.format = format
        self.client = translate.Client()

    def translate_segment(self, segment: TranscriptSegment) -> TranscriptSegment:
        """Translate a single TranscriptSegment using Google Cloud Translation API.

        Uses translate.Client.translate() to convert the segment text to the target language.
        """
        if not segment.text.strip():
            return TranscriptSegment(
                text="",
                is_final=segment.is_final,
                stability=segment.stability,
                words=segment.words,
                confidence=segment.confidence,
                language_code=self.target_language,
            )

        translate_args = {
            "q": segment.text,
            "target_language": self.target_language,
            "format": self.format,
        }
        if self.source_language:
            translate_args["source_language"] = self.source_language

        result = self.client.translate(**translate_args)

        translated_text = result["translatedText"]

        return TranscriptSegment(
            text=translated_text,
            is_final=segment.is_final,
            stability=segment.stability,
            words=segment.words,
            confidence=segment.confidence,
            language_code=self.target_language,
        )

    def translate_event(self, event: StreamingSpeechEvent) -> StreamingSpeechEvent:
        """Translate all segments in a StreamingSpeechEvent via Google Cloud Translation API."""
        translated_segments = [
            self.translate_segment(seg) for seg in event.segments
        ]
        return StreamingSpeechEvent(
            segments=translated_segments,
            raw_response=event.raw_response,
            error=event.error,
        )

    def translate_stream(
        self,
        event_stream,
    ) -> List[StreamingSpeechEvent]:
        """Translate an entire stream of Google Cloud Speech events into the target language.

        Consumes an iterable of StreamingSpeechEvent and returns translated events
        using google.cloud.translate_v2.TranslationClient.
        """
        results = []
        for event in event_stream:
            if event.error:
                results.append(event)
                continue
            translated = self.translate_event(event)
            results.append(translated)
        return results


async def translate_live_captions_async(
    event_stream: AsyncGenerator[StreamingSpeechEvent, None],
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> AsyncGenerator[StreamingSpeechEvent, None]:
    """Async wrapper for live caption translation using Google Cloud Translation API v2.

    Yields translated StreamingSpeechEvent objects for each input event from
    the Google Cloud Speech streaming session.
    """
    translator = LiveCaptionTranslator(
        target_language=target_language,
        source_language=source_language,
    )

    async for event in event_stream:
        if event.error:
            yield event
            continue
        translated = translator.translate_event(event)
        yield translated
