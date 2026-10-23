from google.cloud import speech
from dataclasses import dataclass
from typing import List, Optional, Tuple
import json


@dataclass
class PartialResult:
    transcript: str
    is_final: bool
    confidence: float
    language_code: str
    alternatives: List[str]

    def to_dict(self):
        return {
            "transcript": self.transcript,
            "is_final": self.is_final,
            "confidence": self.confidence,
            "language_code": self.language_code,
            "alternatives": self.alternatives,
        }


class StreamingRecognitionHandler:
    def __init__(self, client=None):
        self.client = client or speech.SpeechClient()
        self.partial_results = []
        self.final_results = []

    def handle_streaming_response(self, response):
        events = []

        for result in response.results:
            if not result.alternatives:
                continue

            alternative = result.alternatives[0]
            transcript = alternative.transcript
            confidence = alternative.confidence or 0.0

            partial_result = PartialResult(
                transcript=transcript,
                is_final=result.is_final,
                confidence=confidence,
                language_code=result.language_code
                if hasattr(result, "language_code")
                else "en-US",
                alternatives=[alt.transcript for alt in result.alternatives[1:]]
                if len(result.alternatives) > 1
                else [],
            )

            if result.is_final:
                self.final_results.append(partial_result)
                events.append(("final", partial_result))
            else:
                self.partial_results.append(partial_result)
                events.append(("partial", partial_result))

        return events

    def process_streaming_requests(self, requests_generator, config):
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        responses = self.client.streaming_recognize(
            config=streaming_config,
            requests=requests_generator,
        )

        for response in responses:
            events = self.handle_streaming_response(response)
            for event_type, result in events:
                yield event_type, result

    def get_latest_partial(self) -> Optional[PartialResult]:
        if self.partial_results:
            return self.partial_results[-1]
        return None

    def get_all_final(self) -> List[PartialResult]:
        return self.final_results.copy()

    def clear_partial(self):
        self.partial_results.clear()

    def merge_partial_to_final(self):
        if self.partial_results:
            latest = self.partial_results[-1]
            self.final_results.append(
                PartialResult(
                    transcript=latest.transcript,
                    is_final=True,
                    confidence=latest.confidence,
                    language_code=latest.language_code,
                    alternatives=latest.alternatives,
                )
            )
            self.clear_partial()

    def export_transcript(self, include_partial=False) -> str:
        transcript_parts = []

        for result in self.final_results:
            transcript_parts.append(result.transcript)

        if include_partial and self.partial_results:
            latest = self.partial_results[-1]
            transcript_parts.append(f"[{latest.transcript}]")

        return " ".join(transcript_parts)
