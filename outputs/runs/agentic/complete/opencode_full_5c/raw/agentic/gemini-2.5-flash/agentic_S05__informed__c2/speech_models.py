import dataclasses
from typing import List, Literal, Optional


@dataclasses.dataclass
class RecognitionConfig:
    encoding: Literal[
        "LINEAR16",
        "FLAC",
        "MULAW",
        "AMR",
        "AMR_NB",
        "AMR_WB",
        "OGG_OPUS",
        "SPEEX_WITH_HEADER_BYTE",
        "WEBM_OPUS",
    ]
    sample_rate_hertz: int
    language_code: str
    max_alternatives: int = 1
    enable_automatic_punctuation: bool = False
    model: Optional[str] = None
    use_enhanced: Optional[bool] = None


@dataclasses.dataclass
class StreamingRecognitionConfig:
    config: RecognitionConfig
    single_utterance: bool = False
    interim_results: bool = True


@dataclasses.dataclass
class SpeechRecognitionAlternative:
    transcript: str
    confidence: float


@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative]
    is_final: bool
    stability: float


@dataclasses.dataclass
class StreamingRecognitionResponse:
    results: List[SpeechRecognitionResult]
    speech_event_type: Optional[
        Literal[
            "SPEECH_EVENT_UNSPECIFIED",
            "END_OF_SINGLE_UTTERANCE",
            "SPEECH_ACTIVITY_BEGIN",
            "SPEECH_ACTIVITY_END",
        ]
    ] = None
