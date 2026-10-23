import dataclasses
from typing import Optional, List, Dict, Any


@dataclasses.dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None


@dataclasses.dataclass
class VoiceSelectionParams:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None


@dataclasses.dataclass
class AudioConfig:
    audio_encoding: str
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None
    sample_rate_hertz: Optional[int] = None


@dataclasses.dataclass
class SynthesizeSpeechRequest:
    input: SynthesisInput
    voice: VoiceSelectionParams
    audio_config: AudioConfig


@dataclasses.dataclass
class TranslateTextRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


@dataclasses.dataclass
class ScriptEmbeddingRequest:
    text: str
    model_name: str = "text-embedding-004"  # Google Cloud Vertex AI Embedding Model


@dataclasses.dataclass
class TranscribeAudioRequest:
    audio_content: bytes
    language_code: str
    sample_rate_hertz: Optional[int] = None
