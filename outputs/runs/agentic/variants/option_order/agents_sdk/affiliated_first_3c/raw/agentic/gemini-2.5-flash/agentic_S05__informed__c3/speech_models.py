from google.cloud import speech

class StreamingSpeechResponse:
    """A simple wrapper for Google Cloud Speech-to-Text streaming responses."""
    def __init__(self, response: speech.StreamingRecognizeResponse):
        self._response = response

    @property
    def is_final(self) -> bool:
        if not self._response.results:
            return False
        return self._response.results[0].is_final

    @property
    def transcript(self) -> str:
        if not self._response.results or not self._response.results[0].alternatives:
            return ""
        return self._response.results[0].alternatives[0].transcript

    @property
    def confidence(self) -> float:
        if not self._response.results or not self._response.results[0].alternatives:
            return 0.0
        return self._response.results[0].alternatives[0].confidence

def create_streaming_request(audio_content: bytes) -> speech.StreamingRecognizeRequest:
    """Creates a Google Cloud Speech-to-Text StreamingRecognizeRequest."""
    return speech.StreamingRecognizeRequest(audio_content=audio_content)
