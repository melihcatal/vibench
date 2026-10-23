from typing import Literal, Dict, Any

class SynthesizeRequest:
    text: str
    text_type: Literal["text", "ssml"]
    output_format: str
    voice_id: str
    region: str

class SynthesizeResponse:
    audio_bytes: bytes
    content_type: str

class VoiceSelectionRequest:
    language_code: str
    gender: Literal["male", "female", "any"]

class VoiceSelectionResponse:
    voices: list[Dict[str, Any]]

class SaveAudioRequest:
    audio_bytes: bytes
    file_name: str
    bucket_name: str
    content_type: str

class SaveAudioResponse:
    s3_uri: str

class TranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str

class TranslateResponse:
    translated_text: str

class SafetyCheckRequest:
    text: str

class SafetyCheckResponse:
    is_safe: bool
    unsafe_categories: list[str]

class EmbeddingRequest:
    text: str

class EmbeddingResponse:
    embedding: list[float]

class TranscriptionRequest:
    audio_uri: str
    language_code: str

class TranscriptionResponse:
    transcript: str
