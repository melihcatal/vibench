from google.cloud import speech
from speech_models import RecognitionRequest
from typing import Iterator, Dict, Any

class SpeechClient:
    def __init__(self):
        self._client = speech.SpeechClient()

    def streaming_recognize(self, request: RecognitionRequest, config: Dict[str, Any] = None) -> Iterator[Dict[str, Any]]:
        recognition_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=request.sample_rate_hz,
            language_code=request.language_code,
            enable_automatic_punctuation=request.enable_automatic_punctuation
        )
        streaming_config = speech.StreamingRecognitionConfig(
            config=recognition_config,
            interim_results=True
        )

        def generate_requests():
            for chunk in request.audio_chunks:
                yield speech.StreamingRecognizeRequest(audio_content=chunk)

        responses = self._client.streaming_recognize(
            config=streaming_config,
            requests=generate_requests()
        )

        for response in responses:
            for result in response.results:
                if result.alternatives:
                    yield {
                        "text": result.alternatives[0].transcript,
                        "is_final": result.is_final,
                        "language_code": result.language_code # This might not be directly available in all results, depends on API
                    }
