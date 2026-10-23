from google.cloud import speech_v1p1beta1 as speech
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
    alternatives: List[Dict[str, Any]]

    def to_dict(self):
        return {
            "transcript": self.transcript,
            "is_final": self.is_final,
            "confidence": self.confidence,
            "stability": self.stability,
            "language_code": self.language_code,
            "alternatives": self.alternatives,
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class StreamingRecognitionHandler:
    def __init__(self, client=None):
        self.client = client or speech.SpeechClient()
        self.partial_results = []
        self.final_results = []

    def process_streaming_response(self, response):
        results = []

        for result in response.results:
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            confidence = result.alternatives[0].confidence
            is_final = result.is_final

            partial_result = PartialResult(
                transcript=transcript,
                is_final=is_final,
                confidence=confidence,
                stability=getattr(result, "stability", None),
                language_code=result.language_code
                if hasattr(result, "language_code")
                else "en-US",
                alternatives=[
                    {"transcript": alt.transcript, "confidence": alt.confidence}
                    for alt in result.alternatives
                ],
            )

            if is_final:
                self.final_results.append(partial_result)
            else:
                self.partial_results.append(partial_result)

            results.append(partial_result)

        return results

    def handle_streaming_events(self, streaming_config, audio_generator):
        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in audio_generator
        )

        responses = self.client.streaming_recognize(streaming_config, requests)

        for response in responses:
            yield self.process_streaming_response(response)

    def get_latest_partial(self):
        if self.partial_results:
            return self.partial_results[-1]
        return None

    def get_all_final(self):
        return self.final_results

    def clear_partial(self):
        self.partial_results.clear()

    def get_combined_transcript(self):
        return " ".join([r.transcript for r in self.final_results])


def handle_partial_results(
    audio_generator, language_code="en-US", enable_punctuation=True
):
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        enable_word_time_offsets=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    handler = StreamingRecognitionHandler(client)

    for results_batch in handler.handle_streaming_events(
        streaming_config, audio_generator
    ):
        for result in results_batch:
            yield result
