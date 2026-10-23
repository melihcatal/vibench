from typing import Any, Dict, List


class SpeechToTextRequest:
    def __init__(self, audio_file: str, language_code: str):
        self.audio_file = audio_file
        self.language_code = language_code

    def to_dict(self) -> Dict[str, Any]:
        return {
            'audio_file': self.audio_file,
            'language_code': self.language_code
        }


class SpeechToTextResponse:
    def __init__(self, transcript: str, confidence: float):
        self.transcript = transcript
        self.confidence = confidence

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            transcript=data['transcript'],
            confidence=data['confidence']
        )


def normalize_transcript(transcript: str) -> str:
    # Placeholder for normalization logic
    return transcript.strip().lower()
