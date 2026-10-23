from google.cloud import speech
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import json


@dataclass
class PartialResult:
    transcript: str
    is_final: bool
    confidence: Optional[float]
    stability: Optional[float]
    language_code: str
    result_end_time: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transcript": self.transcript,
            "is_final": self.is_final,
            "confidence": self.confidence,
            "stability": self.stability,
            "language_code": self.language_code,
            "result_end_time": self.result_end_time,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class StreamingRecognitionHandler:
    def __init__(self, language_code: str = "en-US"):
        self.client = speech.SpeechClient()
        self.language_code = language_code
        self._partial_buffer = []
        self._final_results = []

    def create_streaming_config(
        self,
        enable_automatic_punctuation: bool = True,
        enable_word_time_offsets: bool = False,
        model: str = "latest_long",
    ) -> speech.StreamingRecognitionConfig:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=self.language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
            enable_word_time_offsets=enable_word_time_offsets,
            model=model,
        )

        return speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

    def process_streaming_response(
        self, response: speech.StreamingRecognizeResponse
    ) -> List[PartialResult]:
        results = []

        if not response.results:
            return results

        for result in response.results:
            if not result.alternatives:
                continue

            alternative = result.alternatives[0]

            partial_result = PartialResult(
                transcript=alternative.transcript,
                is_final=result.is_final,
                confidence=alternative.confidence,
                stability=getattr(result, "stability", None),
                language_code=self.language_code,
                result_end_time=getattr(result, "result_end_time", None),
            )

            results.append(partial_result)

            if result.is_final:
                self._final_results.append(partial_result)
                self._partial_buffer = []
            else:
                self._partial_buffer.append(partial_result)

        return results

    def get_latest_partial(self) -> Optional[PartialResult]:
        if not self._partial_buffer:
            return None
        return self._partial_buffer[-1]

    def get_final_results(self) -> List[PartialResult]:
        return self._final_results.copy()

    def clear_buffer(self):
        self._partial_buffer = []

    def handle_realtime_stream(self, audio_stream):
        config = self.create_streaming_config()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in audio_stream
        )

        responses = self.client.streaming_recognize(config, requests)

        for response in responses:
            partial_results = self.process_streaming_response(response)
            yield from partial_results


class PartialResultAggregator:
    def __init__(self):
        self.partial_segments = []
        self.final_segments = []

    def add_partial(self, partial_result: PartialResult):
        if partial_result.is_final:
            self.final_segments.append(partial_result)
            self.partial_segments = []
        else:
            self.partial_segments.append(partial_result)

    def get_combined_transcript(self, include_partials: bool = True) -> str:
        final_text = " ".join([r.transcript for r in self.final_segments])

        if include_partials and self.partial_segments:
            partial_text = " ".join([r.transcript for r in self.partial_segments])
            return f"{final_text} {partial_text}".strip()

        return final_text.strip()

    def get_confidence_score(self) -> float:
        if not self.final_segments:
            return 0.0

        confidences = [
            r.confidence for r in self.final_segments if r.confidence is not None
        ]
        if not confidences:
            return 0.0

        return sum(confidences) / len(confidences)
