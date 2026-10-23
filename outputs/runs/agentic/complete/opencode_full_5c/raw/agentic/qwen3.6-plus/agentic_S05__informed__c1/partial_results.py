from typing import AsyncIterator, Callable, Optional, List

from speech_models import (
    StreamingSpeechEvent,
    StreamingRecognitionResult,
    SpeechEventType,
    RecognitionResultType,
    normalize_transcript_text,
)


class PartialResultHandler:
    def __init__(
        self,
        on_interim: Optional[Callable[[str], None]] = None,
        on_final: Optional[Callable[[str], None]] = None,
        on_speech_start: Optional[Callable[[], None]] = None,
        on_speech_end: Optional[Callable[[], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
    ):
        self.on_interim = on_interim
        self.on_final = on_final
        self.on_speech_start = on_speech_start
        self.on_speech_end = on_speech_end
        self.on_error = on_error
        self._buffer: List[str] = []
        self._current_interim = ""
        self._final_transcripts: List[str] = []

    def handle_event(
        self, event: StreamingSpeechEvent
    ) -> Optional[StreamingRecognitionResult]:
        if event.event_type == SpeechEventType.TRANSCRIPT and event.result:
            result = event.result
            if result.result_type == RecognitionResultType.INTERIM:
                self._current_interim = result.text
                if self.on_interim:
                    self.on_interim(result.text)
            elif result.result_type == RecognitionResultType.FINAL:
                normalized = normalize_transcript_text(result)
                self._final_transcripts.append(normalized)
                self._current_interim = ""
                if self.on_final:
                    self.on_final(normalized)
            return result

        elif event.event_type == SpeechEventType.SPEECH_STARTED:
            if self.on_speech_start:
                self.on_speech_start()

        elif event.event_type == SpeechEventType.SPEECH_ENDED:
            if self.on_speech_end:
                self.on_speech_end()

        return None

    def get_current_interim(self) -> str:
        return self._current_interim

    def get_final_transcripts(self) -> List[str]:
        return list(self._final_transcripts)

    def get_full_transcript(self) -> str:
        return " ".join(self._final_transcripts)

    def reset(self):
        self._buffer.clear()
        self._current_interim = ""
        self._final_transcripts.clear()


async def process_streaming_events(
    event_stream: AsyncIterator[StreamingSpeechEvent],
    handler: Optional[PartialResultHandler] = None,
) -> AsyncIterator[StreamingRecognitionResult]:
    h = handler or PartialResultHandler()

    async for event in event_stream:
        result = h.handle_event(event)
        if result is not None:
            yield result


def aggregate_final_results(
    results: List[StreamingRecognitionResult],
) -> str:
    finals = [r for r in results if r.is_final]
    texts = [normalize_transcript_text(r) for r in finals]
    return " ".join(t for t in texts if t)


def extract_interim_text(
    results: List[StreamingRecognitionResult],
) -> str:
    interims = [r for r in results if not r.is_final]
    if interims:
        return interims[-1].text
    return ""
