from dataclasses import dataclass


@dataclass
class VoiceConfig:
    language_code: str = "en-US"
    name: str = "en-US-Standard-A"
    ssml_gender: str = "NEUTRAL"


@dataclass
class SynthesisRequest:
    text: str
    voice_config: VoiceConfig
    audio_encoding: str = "LINEAR16"


@dataclass
class TranslationRequest:
    text_content: str
    target_language_code: str
    parent: str  # Format: projects/PROJECT_ID/locations/global


@dataclass
class ContentSafetyRequest:
    text: str


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str
