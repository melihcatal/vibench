from typing import Literal, Optional, Dict, Any, List

class VoiceSelectionRequest:
    def __init__(self, language_code: str, gender: Optional[Literal["MALE", "FEMALE", "NEUTRAL"]] = None, name: Optional[str] = None):
        self.language_code = language_code
        self.gender = gender
        self.name = name

class VoiceInfo:
    def __init__(self, name: str, language_codes: List[str], gender: Literal["MALE", "FEMALE", "NEUTRAL"], natural_sample_rate_hertz: int):
        self.name = name
        self.language_codes = language_codes
        self.gender = gender
        self.natural_sample_rate_hertz = natural_sample_rate_hertz

class SynthesisRequest:
    def __init__(self, text: str, voice_name: str, language_code: str, audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"] = "MP3", speaking_rate: Optional[float] = None, pitch: Optional[float] = None):
        self.text = text
        self.voice_name = voice_name
        self.language_code = language_code
        self.audio_encoding = audio_encoding
        self.speaking_rate = speaking_rate
        self.pitch = pitch

class SSMLSynthesisRequest:
    def __init__(self, ssml: str, voice_name: str, language_code: str, audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"] = "MP3", speaking_rate: Optional[float] = None, pitch: Optional[float] = None):
        self.ssml = ssml
        self.voice_name = voice_name
        self.language_code = language_code
        self.audio_encoding = audio_encoding
        self.speaking_rate = speaking_rate
        self.pitch = pitch

class AudioResult:
    def __init__(self, audio_content: bytes, audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"]):
        self.audio_content = audio_content
        self.audio_encoding = audio_encoding

class AudioSaveRequest:
    def __init__(self, audio_content: bytes, filename: str, content_type: str):
        self.audio_content = audio_content
        self.filename = filename
        self.content_type = content_type

class AudioSaveResult:
    def __init__(self, url: str, size_bytes: int):
        self.url = url
        self.size_bytes = size_bytes

class TranslationRequest:
    def __init__(self, text: str, source_lang: str, target_lang: str):
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang

class TranslationResult:
    def __init__(self, translated_text: str, source_lang: str, target_lang: str):
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang

class SafetyCheckRequest:
    def __init__(self, text: str):
        self.text = text

class SafetyCheckResult:
    def __init__(self, is_safe: bool, moderation_categories: Dict[str, Any]):
        self.is_safe = is_safe
        self.moderation_categories = moderation_categories

class EmbeddingRequest:
    def __init__(self, text: str):
        self.text = text

class EmbeddingResult:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding

class TranscriptionRequest:
    def __init__(self, audio_content: bytes, language_code: str, sample_rate_hertz: Optional[int] = None, audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS", "FLAC", "MULAW", "AMR", "AMR_WB"] = "MP3"):
        self.audio_content = audio_content
        self.language_code = language_code
        self.sample_rate_hertz = sample_rate_hertz
        self.audio_encoding = audio_encoding

class TranscriptionResult:
    def __init__(self, transcript: str, confidence: float):
        self.transcript = transcript
        self.confidence = confidence
