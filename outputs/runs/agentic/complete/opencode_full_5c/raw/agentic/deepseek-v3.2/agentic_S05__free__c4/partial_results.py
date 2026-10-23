from google.cloud import speech_v1p1beta1 as speech
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import json


@dataclass
class PartialResult:
    transcript: str
    is_final: bool
    confidence: float
    language_code: str
    alternatives: List[Dict[str, Any]]
    stability: float = 0.0


class StreamingResultHandler:
    def __init__(self, language_code="en-US"):
        self.client = speech.SpeechClient()
        self.language_code = language_code
        self.partial_results = []
        self.final_results = []

    def process_streaming_response(self, response):
        results = []
        for result in response.results:
            if not result.alternatives:
                continue

            alternative = result.alternatives[0]
            partial_result = PartialResult(
                transcript=alternative.transcript,
                is_final=result.is_final,
                confidence=alternative.confidence,
                language_code=self.language_code,
                alternatives=[
                    {"transcript": alt.transcript, "confidence": alt.confidence}
                    for alt in result.alternatives
                ],
                stability=getattr(result, "stability", 0.0),
            )

            if result.is_final:
                self.final_results.append(partial_result)
            else:
                self.partial_results.append(partial_result)

            results.append(partial_result)

        return results

    def get_latest_partial(self) -> Optional[PartialResult]:
        if self.partial_results:
            return self.partial_results[-1]
        return None

    def get_all_final(self) -> List[PartialResult]:
        return self.final_results.copy()

    def clear_partials(self):
        self.partial_results.clear()

    def merge_partial_with_context(
        self, partial: PartialResult, context: str = ""
    ) -> str:
        if context:
            return f"{context} {partial.transcript}"
        return partial.transcript

    def format_for_display(self, result: PartialResult) -> str:
        status = "FINAL" if result.is_final else "PARTIAL"
        confidence_str = f"{result.confidence:.2%}" if result.confidence else "N/A"
        return f"[{status}] {result.transcript} (conf: {confidence_str})"

    def save_results(self, filename: str):
        data = {
            "final_results": [
                {
                    "transcript": r.transcript,
                    "confidence": r.confidence,
                    "language_code": r.language_code,
                }
                for r in self.final_results
            ],
            "partial_results": [
                {
                    "transcript": r.transcript,
                    "confidence": r.confidence,
                    "stability": r.stability,
                }
                for r in self.partial_results
            ],
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
