import dataclasses
import enum

@dataclasses.dataclass
class AudioChunk:
    chunk_id: int
    content: bytes
    sequence_number: int
    is_last_chunk: bool = False

@dataclasses.dataclass
class TranscriptSegment:
    id: int
    seek: int
    start: float
    end: float
    text: str
    tokens: list[int]
    temperature: float
    avg_logprob: float
    compression_ratio: float
    no_speech_prob: float

@dataclasses.dataclass
class TranscriptResponse:
    text: str
    segments: list[TranscriptSegment]
    language: str

class RecognitionLanguage(enum.Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"

@dataclasses.dataclass
class RecognitionConfig:
    language: RecognitionLanguage
    enable_automatic_punctuation: bool = True
    profanity_filter: bool = False

@dataclasses.dataclass
class LiveCaption:
    text: str
    language: str
    is_partial: bool
