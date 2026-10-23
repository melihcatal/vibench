from dataclasses import dataclass


@dataclass
class StreamingRecognitionConfig:
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
