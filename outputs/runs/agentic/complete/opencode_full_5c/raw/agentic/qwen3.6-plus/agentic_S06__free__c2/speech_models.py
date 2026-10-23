from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class TTSRequest:
    input_text: str
    voice: str = "alloy"
    model: str = "tts-1"
    response_format: str = "mp3"
    speed: float = 1.0
    hd: bool = False


@dataclass
class SSMLRequest:
    ssml: str
    voice: str = "alloy"
    model: str = "tts-1"
    response_format: str = "mp3"
    speed: float = 1.0
    hd: bool = False


@dataclass
class TTSResponse:
    audio_bytes: bytes
    content_type: str
    model_used: str
    voice_used: str
    duration_ms: Optional[int] = None
    character_count: int = 0


@dataclass
class VoiceInfo:
    voice_id: str
    name: str
    locale: str
    gender: str
    sample_rate: int = 24000
    supported_formats: List[str] = field(
        default_factory=lambda: ["mp3", "opus", "aac", "flac", "wav", "pcm"]
    )


@dataclass
class VoiceSelectionRequest:
    locale: str
    gender: Optional[str] = None
    voice_name: Optional[str] = None


@dataclass
class TranslateRequest:
    text: str
    source_language: str = "auto"
    target_language: str = "en"
    model: str = "gpt-4o"


@dataclass
class TranslateResponse:
    translated_text: str
    source_language: str
    target_language: str
    model_used: str


@dataclass
class SafetyRequest:
    text: str
    categories: Optional[List[str]] = None


@dataclass
class SafetyResponse:
    is_safe: bool
    flagged_categories: List[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)
    model_used: str = ""


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-3-small"


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model_used: str
    dimensions: int


@dataclass
class TranscriptRequest:
    audio_bytes: bytes
    language: str = "en"
    model: str = "whisper-1"
    response_format: str = "text"


@dataclass
class TranscriptResponse:
    text: str
    language: str
    model_used: str
    duration_seconds: Optional[float] = None


def normalize_tts_request(req: TTSRequest) -> Dict[str, Any]:
    payload = {
        "model": req.model,
        "input": req.input_text,
        "voice": req.voice,
        "response_format": req.response_format,
        "speed": req.speed,
    }
    return payload


def normalize_ssml_request(req: SSMLRequest) -> Dict[str, Any]:
    payload = {
        "model": req.model,
        "input": req.ssml,
        "voice": req.voice,
        "response_format": req.response_format,
        "speed": req.speed,
    }
    return payload


def normalize_translate_request(req: TranslateRequest) -> List[Dict[str, str]]:
    messages = [
        {
            "role": "system",
            "content": f"Translate the following text to {req.target_language}. Only return the translated text.",
        },
        {"role": "user", "content": req.text},
    ]
    return messages


def normalize_safety_request(req: SafetyRequest) -> List[Dict[str, str]]:
    categories = req.categories or ["hate", "self-harm", "sexual", "violence"]
    categories_str = ", ".join(categories)
    messages = [
        {
            "role": "system",
            "content": f"Analyze the text for unsafe content in these categories: {categories_str}. Return a JSON object with 'is_safe' (boolean), 'flagged_categories' (list), and 'scores' (dict of category to float 0-1).",
        },
        {"role": "user", "content": req.text},
    ]
    return messages


def normalize_embedding_request(req: EmbeddingRequest) -> Dict[str, Any]:
    return {
        "input": req.text,
        "model": req.model,
    }


def normalize_transcript_request(req: TranscriptRequest) -> Dict[str, Any]:
    return {
        "model": req.model,
        "file": ("audio.mp3", req.audio_bytes, "audio/mpeg"),
        "language": req.language,
        "response_format": req.response_format,
    }
