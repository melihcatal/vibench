import dataclasses

@dataclasses.dataclass
class StreamingRecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    interim_results: bool = True

@dataclasses.dataclass
class AudioChunk:
    content: bytes
    sample_rate_hertz: int
    encoding: str
