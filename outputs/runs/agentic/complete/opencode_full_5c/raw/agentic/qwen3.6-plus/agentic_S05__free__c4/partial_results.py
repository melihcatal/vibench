from typing import List, Optional, Callable, Dict, Any
from collections import defaultdict

from speech_models import (
    RecognitionResult,
    ResultType,
    merge_transcripts,
)


class StreamingResultHandler:
    def __init__(
        self,
        on_interim: Optional[Callable[[RecognitionResult], None]] = None,
        on_final: Optional[Callable[[RecognitionResult], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
    ):
        self._on_interim = on_interim
        self._on_final = on_final
        self._on_error = on_error
        self._results: List[RecognitionResult] = []
        self._interim_buffer: Dict[str, RecognitionResult] = {}
        self._final_transcripts: List[str] = []
        self._total_words: int = 0
        self._total_confidence: float = 0.0

    def handle_response(self, result: RecognitionResult):
        if result.is_final:
            self._handle_final(result)
        else:
            self._handle_interim(result)

    def _handle_interim(self, result: RecognitionResult):
        self._interim_buffer[result.result_id] = result
        if self._on_interim:
            self._on_interim(result)

    def _handle_final(self, result: RecognitionResult):
        if result.result_id in self._interim_buffer:
            del self._interim_buffer[result.result_id]

        self._results.append(result)
        self._final_transcripts.append(result.best_transcript)
        self._total_words += len(result.best_transcript.split())
        self._total_confidence += result.best_confidence

        if self._on_final:
            self._on_final(result)

    def handle_error(self, error: Exception):
        if self._on_error:
            self._on_error(error)

    def get_current_transcript(self) -> str:
        return merge_transcripts(self._results)

    def get_interim_transcript(self) -> str:
        parts = []
        for r in self._interim_buffer.values():
            parts.append(r.best_transcript)
        return " ".join(parts)

    def get_full_transcript(self) -> str:
        return " ".join(self._final_transcripts)

    def get_average_confidence(self) -> float:
        if not self._results:
            return 0.0
        return self._total_confidence / len(self._results)

    def get_word_count(self) -> int:
        return self._total_words

    def get_results_summary(self) -> Dict[str, Any]:
        return {
            "final_count": len(self._results),
            "interim_count": len(self._interim_buffer),
            "total_words": self._total_words,
            "average_confidence": self.get_average_confidence(),
            "full_transcript": self.get_full_transcript(),
        }

    def reset(self):
        self._results.clear()
        self._interim_buffer.clear()
        self._final_transcripts.clear()
        self._total_words = 0
        self._total_confidence = 0.0


class PartialResultAggregator:
    def __init__(self, max_interim_age_sec: float = 5.0):
        self._handler = StreamingResultHandler()
        self._max_interim_age_sec = max_interim_age_sec
        self._pending_finals: List[RecognitionResult] = []

    def process_streaming_event(self, result: RecognitionResult):
        if result.stability >= 0.85 and not result.is_final:
            self._pending_finals.append(result)
            return

        if result.is_final:
            for pending in self._pending_finals:
                self._handler.handle_response(pending)
            self._pending_finals.clear()

        self._handler.handle_response(result)

    def get_handler(self) -> StreamingResultHandler:
        return self._handler

    def flush_pending(self):
        for pending in self._pending_finals:
            self._handler.handle_response(pending)
        self._pending_finals.clear()


def create_default_handler(
    on_interim_text: Optional[Callable[[str], None]] = None,
    on_final_text: Optional[Callable[[str], None]] = None,
) -> StreamingResultHandler:
    def wrap_interim(result: RecognitionResult):
        if on_interim_text:
            on_interim_text(result.best_transcript)

    def wrap_final(result: RecognitionResult):
        if on_final_text:
            on_final_text(result.best_transcript)

    return StreamingResultHandler(
        on_interim=wrap_interim,
        on_final=wrap_final,
    )
