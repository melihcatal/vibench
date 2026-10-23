import dataclasses
from typing import Optional


@dataclasses.dataclass
class RecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    max_alternatives: int = 1
    enable_automatic_punctuation: bool = True


@dataclasses.dataclass
class StreamingRecognitionConfig:
    config: RecognitionConfig = dataclasses.field(default_factory=RecognitionConfig)
    interim_results: bool = True


@dataclasses.dataclass
class StreamingRecognizeRequest:
    audio_content: Optional[bytes] = None
    streaming_config: Optional[StreamingRecognitionConfig] = None
