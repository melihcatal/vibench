from google.cloud import speech_v1p1beta1 as speech
from dataclasses import dataclass
from typing import List, Optional
import time


@dataclass
class PartialResult:
    transcript: str
    is_final: bool
    stability: float
    confidence: Optional[float]
    word_offsets: List[dict]
    language_code: str
    result_end_time: float


class StreamingRecognitionHandler:
    def __init__(self, language_code="en-US", enable_punctuation=True):
        self.client = speech.SpeechClient()
        self.language_code = language_code
        self.enable_punctuation = enable_punctuation
        self.partial_results = []
        self.final_results = []

    def create_streaming_config(self):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=self.language_code,
            enable_automatic_punctuation=self.enable_punctuation,
            enable_word_time_offsets=True,
            model="latest_long",
            use_enhanced=True,
        )

        return speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
            speech_contexts=[
                speech.SpeechContext(phrases=["Google", "Assistant", "OK"])
            ],
        )

    def process_streaming_response(self, responses):
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            alternative = result.alternatives[0]

            word_offsets = []
            if alternative.words:
                for word_info in alternative.words:
                    word_offsets.append(
                        {
                            "word": word_info.word,
                            "start_time": word_info.start_time.total_seconds(),
                            "end_time": word_info.end_time.total_seconds(),
                        }
                    )

            partial_result = PartialResult(
                transcript=alternative.transcript,
                is_final=result.is_final,
                stability=result.stability if hasattr(result, "stability") else 0.0,
                confidence=alternative.confidence if result.is_final else None,
                word_offsets=word_offsets,
                language_code=self.language_code,
                result_end_time=result.result_end_time.total_seconds()
                if hasattr(result, "result_end_time")
                else time.time(),
            )

            if result.is_final:
                self.final_results.append(partial_result)
                yield {"type": "final", "result": partial_result}
            else:
                self.partial_results.append(partial_result)
                yield {"type": "partial", "result": partial_result}

    def handle_audio_stream(self, audio_generator):
        config = self.create_streaming_config()

        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in audio_generator
        )

        responses = self.client.streaming_recognize(config, requests)

        for event in self.process_streaming_response(responses):
            yield event

    def get_all_partial_results(self):
        return self.partial_results

    def get_all_final_results(self):
        return self.final_results

    def get_combined_transcript(self):
        return " ".join([r.transcript for r in self.final_results])


def handle_partial_final_events(audio_chunks, language="en-US"):
    handler = StreamingRecognitionHandler(language_code=language)

    for event in handler.handle_audio_stream(audio_chunks):
        result = event["result"]

        if event["type"] == "partial":
            print(f"Partial: {result.transcript} (stability: {result.stability:.2f})")
        else:
            print(f"Final: {result.transcript} (confidence: {result.confidence:.2f})")

        yield event
