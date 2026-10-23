from typing import List, Dict, Any, Optional
import json

class TranscriptionAlternative:
    """Represents a single transcription alternative with its confidence."""
    def __init__(self, transcript: str, confidence: Optional[float] = None):
        self.transcript = transcript
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {"transcript": self.transcript, "confidence": self.confidence}

class TranscriptionResult:
    """Represents a single result from a speech-to-text service, potentially with multiple alternatives."""
    def __init__(self, alternatives: List[TranscriptionAlternative], is_final: bool, stability: Optional[float] = None):
        self.alternatives = alternatives
        self.is_final = is_final
        self.stability = stability # Common in some streaming APIs for partial results

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alternatives": [alt.to_dict() for alt in self.alternatives],
            "is_final": self.is_final,
            "stability": self.stability,
        }

class StreamingRecognitionRequest:
    """A generic representation of a streaming recognition request."""
    def __init__(self, audio_chunk: bytes, language_code: str = "en-US", sample_rate_hertz: int = 16000):
        self.audio_chunk = audio_chunk
        self.language_code = language_code
        self.sample_rate_hertz = sample_rate_hertz

    def to_dict(self) -> Dict[str, Any]:
        # Note: audio_chunk bytes cannot be directly JSON serialized, 
        # would need base64 encoding for typical API calls.
        return {
            "language_code": self.language_code,
            "sample_rate_hertz": self.sample_rate_hertz,
            "audio_chunk_length": len(self.audio_chunk)
        }

class TranscriptionNormalizer:
    """Provides utility methods to normalize provider-specific responses into a common format."""

    @staticmethod
    def from_openai_response(response: Any) -> List[TranscriptionResult]:
        """Normalizes OpenAI Whisper transcription response (assuming non-streaming for now)."""
        # OpenAI's current client for `client.audio.transcriptions.create` returns a Transcription object.
        # For streaming, the structure might be different or require manual chunking/processing.
        if hasattr(response, 'text'):
            return [TranscriptionResult(
                alternatives=[TranscriptionAlternative(transcript=response.text)],
                is_final=True # Assuming final for this API call type
            )]
        elif isinstance(response, dict) and 'text' in response:
            return [TranscriptionResult(
                alternatives=[TranscriptionAlternative(transcript=response['text'])],
                is_final=True
            )]
        return []

    @staticmethod
    def from_google_cloud_response(response: Any) -> List[TranscriptionResult]:
        """Normalizes Google Cloud Speech-to-Text streaming recognition response."""
        results = []
        for res in response.results:
            alternatives = [
                TranscriptionAlternative(alt.transcript, alt.confidence)
                for alt in res.alternatives
            ]
            results.append(TranscriptionResult(
                alternatives=alternatives,
                is_final=res.is_final,
                stability=getattr(res, 'stability', None)
            ))
        return results

    @staticmethod
    def from_aws_transcribe_response(response: Dict[str, Any]) -> List[TranscriptionResult]:
        """Normalizes AWS Transcribe streaming WebSocket response."""
        results = []
        if "Transcript" in response and "Results" in response["Transcript"]:
            for res in response["Transcript"]["Results"]:
                alternatives = []
                for alt in res["Alternatives"]:
                    alternatives.append(TranscriptionAlternative(alt["Transcript"])) # AWS may not always provide confidence in streaming partials
                results.append(TranscriptionResult(
                    alternatives=alternatives,
                    is_final=not res["IsPartial"]
                ))
        return results

    @staticmethod
    def from_ibm_watson_response(response: Dict[str, Any]) -> List[TranscriptionResult]:
        """Normalizes IBM Watson Speech to Text streaming WebSocket response."""
        results = []
        if "results" in response:
            for res in response["results"]:
                alternatives = []
                for alt in res["alternatives"]:
                    alternatives.append(TranscriptionAlternative(alt["transcript"], alt.get("confidence")))
                results.append(TranscriptionResult(
                    alternatives=alternatives,
                    is_final=res["final"]
                ))
        return results

