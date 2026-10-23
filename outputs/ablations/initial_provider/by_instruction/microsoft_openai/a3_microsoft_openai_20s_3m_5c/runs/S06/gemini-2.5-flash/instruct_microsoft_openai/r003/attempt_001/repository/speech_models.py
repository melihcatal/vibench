from dataclasses import dataclass

@dataclass
class SynthesisRequest:
    text: str
    voice_name: str = "en-US-JennyNeural"
    output_format: str = "audio-16khz-128kbitrate-mono-mp3"

@dataclass
class SynthesisSSMLRequest:
    ssml: str
    output_format: str = "audio-16khz-128kbitrate-mono-mp3"

@dataclass
class VoiceInfo:
    short_name: str
    display_name: str
    locale: str
    gender: str
    sample_rate_hertz: str
    voice_type: str

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: str = "en"

@dataclass
class SafetyCheckRequest:
    text: str

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class TranscriptionRequest:
    audio_bytes: bytes
    language_code: str = "en-US"
