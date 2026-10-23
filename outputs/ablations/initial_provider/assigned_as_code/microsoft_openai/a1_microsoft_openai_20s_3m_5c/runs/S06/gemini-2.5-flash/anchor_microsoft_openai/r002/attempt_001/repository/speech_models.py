import dataclasses

@dataclasses.dataclass
class SynthesisPayload:
    text: str
    voice: str = "en-US-JennyNeural"
    output_format: str = "Audio16Khz32KBitRateMonoMp3"

@dataclasses.dataclass
class SSMLSynthesisPayload:
    ssml: str
    output_format: str = "Audio16Khz32KBitRateMonoMp3"

@dataclasses.dataclass
class VoiceSelectionPayload:
    locale: str = "en-US"

@dataclasses.dataclass
class AudioSavePayload:
    audio_bytes: bytes
    file_path: str

@dataclasses.dataclass
class TranslationPayload:
    text: str
    target_language: str
    source_language: str = "en"

@dataclasses.dataclass
class SafetyCheckPayload:
    text: str

@dataclasses.dataclass
class EmbeddingPayload:
    text: str

@dataclasses.dataclass
class TranscriptionPayload:
    audio_bytes: bytes
    language: str = "en-US"
