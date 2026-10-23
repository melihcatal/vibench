import asyncio
from typing import AsyncGenerator, AsyncIterable, Callable, List, Optional, Tuple

from speech_models import (
    StreamingTranscriptEvent,
    StreamingRecognitionResult,
    TranscriptAlternative,
    WordInfo,
    extract_interim_text,
    merge_final_transcripts,
)


class PartialResultsHandler:
    def __init__(
        self,
        on_interim: Optional[Callable[[str], None]] = None,
        on_final: Optional[Callable[[str], float], None]] = None,
        on_word: Optional[Callable[[WordInfo], None]] = None,
        on_speech_event: Optional[Callable[[dict], None]] = None,
    ):
        self._on_interim = on_interim
        self._on_final = on_final
        self._on_word = on_word
        self._on_speech_event = on_speech_event
        self._interim_buffer: List[str] = []
        self._final_transcripts: List[str] = []
        self._all_words: List[WordInfo] = []
        self._speech_activity_events: List[dict] = []

    def process_event(self, event: StreamingTranscriptEvent) -> dict:
        result = event.result
        output = {
            "type": "interim" if event.is_interim else "final",
            "text": event.text,
            "confidence": event.confidence,
            "is_final": result.is_final,
        }

        if event.is_interim:
            interim_text = extract_interim_text(event)
            self._interim_buffer.append(interim_text)
            if self._on_interim:
                self._on_interim(interim_text)
            output["interim_text"] = interim_text
        else:
            final_text = event.text
            self._final_transcripts.append(final_text)
            if self._on_final:
                self._on_final(final_text, event.confidence)
            output["final_text"] = final_text

        if result.alternatives:
            for alt in result.alternatives:
                for word in alt.words:
                    self._all_words.append(word)
                    if self._on_word:
                        self._on_word(word)

        if hasattr(result, "speech_event_type") and result.speech_event_type:
            speech_event = {"type": str(result.speech_event_type)}
            self._speech_activity_events.append(speech_event)
            if self._on_speech_event:
                self._on_speech_event(speech_event)

        return output

    @property
    def final_transcript(self) -> str:
        return merge_final_transcripts(
            [
                StreamingTranscriptEvent(
                    result=StreamingRecognitionResult(
                        is_final=True,
                        alternatives=[TranscriptAlternative(text=t)],
                    )
                )
                for t in self._final_transcripts
            ]
        )

    @property
    def current_interim(self) -> str:
        return " ".join(self._interim_buffer).strip()

    @property
    def all_words(self) -> List[WordInfo]:
        return self._all_words

    @property
    def speech_events(self) -> List[dict]:
        return self._speech_activity_events

    def reset(self):
        self._interim_buffer.clear()
        self._final_transcripts.clear()
        self._all_words.clear()
        self._speech_activity_events.clear()


async def process_streaming_events(
    events: AsyncIterable[StreamingTranscriptEvent],
    handler: Optional[PartialResultsHandler] = None,
) -> AsyncGenerator[dict, None]:
    if handler is None:
        handler = PartialResultsHandler()

    async for event in events:
        result = handler.process_event(event)
        yield result


def collect_final_transcripts(
    processed_results: List[dict],
) -> str:
    finals = [r.get("final_text", "") for r in processed_results if r.get("is_final")]
    return " ".join(finals).strip()


def collect_interim_updates(
    processed_results: List[dict],
) -> List[str]:
    return [
        r.get("interim_text", "")
        for r in processed_results
        if r.get("type") == "interim"
    ]
