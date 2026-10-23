from dataclasses import dataclass


@dataclass
class SpeechRecognitionResult:
    text: str
    is_final: bool
    language: str = "en-US"
