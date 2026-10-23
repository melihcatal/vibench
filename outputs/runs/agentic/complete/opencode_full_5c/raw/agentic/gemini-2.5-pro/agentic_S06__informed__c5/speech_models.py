from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class SpeechRequest:
    text: str
    voice: Optional[str] = None
    language_code: str = "en-US"
    ssml: bool = False


@dataclass
class Voice:
    name: str
    language_codes: List[str]
    ssml_gender: str
    natural_sample_rate_hertz: int

    def to_dict(self):
        return {
            "name": self.name,
            "language_codes": self.language_codes,
            "ssml_gender": self.ssml_gender,
            "natural_sample_rate_hertz": self.natural_sample_rate_hertz,
        }


@dataclass
class SynthesizeResponse:
    audio_content: bytes
    request: SpeechRequest


@dataclass
class TranslationRequest:
    text: str
    target_lang: str


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_lang: str


@dataclass
class SafetyCheckRequest:
    text: str


@dataclass
class SafetyCheckResponse:
    is_safe: bool
    details: Optional[Dict] = None


@dataclass
class EmbeddingRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]


@dataclass
class TranscriptionRequest:
    audio_path: str


@dataclass
class TranscriptionResponse:
    text: str
