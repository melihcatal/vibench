import json

class StreamingRecognitionResult:
    """Helper class to normalize streaming recognition results."""
    def __init__(self, response_json):
        self._response_json = response_json

    @property
    def transcript(self):
        for result in self._response_json.results:
            if result.alternatives:
                return result.alternatives[0].transcript
        return ""

    @property
    def is_final(self):
        for result in self._response_json.results:
            return result.is_final
        return False

    @property
    def confidence(self):
        for result in self._response_json.results:
            if result.alternatives:
                return result.alternatives[0].confidence
        return 0.0

    def to_dict(self):
        return {
            "text": self.transcript,
            "is_final": self.is_final,
            "confidence": self.confidence,
        }
