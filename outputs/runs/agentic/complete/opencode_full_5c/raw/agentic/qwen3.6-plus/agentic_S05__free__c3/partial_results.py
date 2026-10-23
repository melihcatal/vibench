from typing import List, Optional, Callable, Awaitable
from dataclasses import dataclass, field
from google.cloud import speech_v1p1beta1 as speech


@dataclass
class PartialTranscript:
    text: str
    is_final: bool
    confidence: float
    stability: float
    start_time: float
    end_time: float
    words: List[dict] = field(default_factory=list)


@dataclass
class StreamingRecognitionSession:
    partial_results: List[PartialTranscript] = field(default_factory=list)
    final_results: List[PartialTranscript] = field(default_factory=list)
    on_partial: Optional[Callable[[PartialTranscript], None]] = None
    on_final: Optional[Callable[[PartialTranscript], None]] = None
    _current_partial: Optional[PartialTranscript] = None

    def process_response(
        self, response: speech.StreamingRecognizeResponse
    ) -> List[PartialTranscript]:
        new_results = []
        for result in response.results:
            if not result.alternatives:
                continue

            best_alt = result.alternatives[0]
            start_time = (
                result.result_start_time.total_seconds()
                if result.result_start_time
                else 0.0
            )
            end_time = (
                result.result_end_time.total_seconds()
                if result.result_end_time
                else 0.0
            )

            word_info = []
            for word in best_alt.words:
                word_info.append(
                    {
                        "word": word.word,
                        "start_time": word.start_time.total_seconds()
                        if word.start_time
                        else 0.0,
                        "end_time": word.end_time.total_seconds()
                        if word.end_time
                        else 0.0,
                        "confidence": word.confidence,
                    }
                )

            partial = PartialTranscript(
                text=best_alt.transcript,
                is_final=result.is_final,
                confidence=best_alt.confidence,
                stability=result.stability,
                start_time=start_time,
                end_time=end_time,
                words=word_info,
            )

            if result.is_final:
                self.final_results.append(partial)
                if self.on_final:
                    self.on_final(partial)
            else:
                self._current_partial = partial
                self.partial_results.append(partial)
                if self.on_partial:
                    self.on_partial(partial)

            new_results.append(partial)

        return new_results

    def get_latest_final(self) -> Optional[PartialTranscript]:
        return self.final_results[-1] if self.final_results else None

    def get_latest_partial(self) -> Optional[PartialTranscript]:
        return self._current_partial

    def get_full_transcript(self, include_partial: bool = True) -> str:
        parts = [r.text for r in self.final_results]
        if include_partial and self._current_partial:
            parts.append(self._current_partial.text)
        return " ".join(parts)

    def get_word_timings(self) -> List[dict]:
        all_words = []
        for result in self.final_results:
            all_words.extend(result.words)
        if self._current_partial:
            all_words.extend(self._current_partial.words)
        return all_words

    def reset(self):
        self.partial_results.clear()
        self.final_results.clear()
        self._current_partial = None
