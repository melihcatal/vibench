
from typing import List, Dict, Any

class StreamingSpeechToTextRequest:
    """
    Represents a request for streaming speech-to-text.
    """
    def __init__(self, audio_content: bytes, encoding: str, sample_rate_hertz: int,
                 language_code: str, interim_results: bool = True):
        self.audio_content = audio_content
        self.encoding = encoding
        self.sample_rate_hertz = sample_rate_hertz
        self.language_code = language_code
        self.interim_results = interim_results

    def to_dict(self) -> Dict[str, Any]:
        """Converts the request object to a dictionary for API consumption."""
        return {
            "audio_content": self.audio_content,
            "config": {
                "encoding": self.encoding,
                "sample_rate_hertz": self.sample_rate_hertz,
                "language_code": self.language_code,
                "interim_results": self.interim_results,
            },
        }

class StreamingSpeechToTextResponse:
    """
    Represents a response from streaming speech-to-text.
    """
    def __init__(self, transcript: str, confidence: float, is_final: bool):
        self.transcript = transcript
        self.confidence = confidence
        self.is_final = is_final

    @classmethod
    def from_dict(cls, response_dict: Dict[str, Any]) -> 'StreamingSpeechToTextResponse':
        """Creates a response object from a dictionary received from an API."""
        result = response_dict.get("results", [{}])[0]
        alternatives = result.get("alternatives", [{}])
        if alternatives:
            transcript = alternatives[0].get("transcript", "")
            confidence = alternatives[0].get("confidence", 0.0)
            is_final = result.get("is_final", False)
            return cls(transcript, confidence, is_final)
        return cls("", 0.0, False)

def normalize_response(raw_response: Dict[str, Any]) -> StreamingSpeechToTextResponse:
    """
    Normalizes a raw API response into a StreamingSpeechToTextResponse object.
    """
    return StreamingSpeechToTextResponse.from_dict(raw_response)
