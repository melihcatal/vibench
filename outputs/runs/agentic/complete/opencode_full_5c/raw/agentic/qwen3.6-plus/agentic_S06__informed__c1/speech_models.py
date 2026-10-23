from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum


class OutputFormat(str, Enum):
    MP3 = "mp3_44100_128"
    MP3_LOW = "mp3_44100_64"
    PCM = "pcm_16000"
    PCM_22K = "pcm_22050"
    PCM_24K = "pcm_24000"
    PCM_44K = "pcm_44100"
    ULAW = "ulaw_8000"
    ALAW = "alaw_8000"


class StabilityPreset(str, Enum):
    LOW = 0.0
    MEDIUM = 0.5
    HIGH = 0.75
    VERY_HIGH = 1.0


@dataclass
class TTSRequest:
    text: str
    voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    model_id: str = "eleven_multilingual_v2"
    output_format: OutputFormat = OutputFormat.MP3
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "text": self.text,
            "model_id": self.model_id,
            "output_format": self.output_format.value,
            "voice_settings": {
                "stability": self.stability,
                "similarity_boost": self.similarity_boost,
                "style": self.style,
                "use_speaker_boost": self.use_speaker_boost,
            },
        }
        return payload


@dataclass
class SSMLRequest:
    ssml: str
    voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    model_id: str = "eleven_multilingual_v2"
    output_format: OutputFormat = OutputFormat.MP3
    stability: float = 0.5
    similarity_boost: float = 0.75

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "text": self.ssml,
            "model_id": self.model_id,
            "output_format": self.output_format.value,
            "voice_settings": {
                "stability": self.stability,
                "similarity_boost": self.similarity_boost,
            },
        }
        return payload


@dataclass
class VoiceInfo:
    voice_id: str
    name: str
    category: str
    description: str
    labels: Dict[str, str] = field(default_factory=dict)
    preview_url: Optional[str] = None
    available_for_tiers: List[str] = field(default_factory=list)
    settings: Optional[Dict[str, Any]] = None


@dataclass
class TTSResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    character_count: int = 0
    voice_id: str = ""
    model_id: str = ""


@dataclass
class TranslationRequest:
    text: str
    source_lang: str = "en"
    target_lang: str = "es"


@dataclass
class TranslationResponse:
    translated_text: str
    source_lang: str
    target_lang: str
    character_count: int = 0


@dataclass
class SafetyCheckRequest:
    text: str
    languages: List[str] = field(default_factory=lambda: ["en"])
    attributes: List[str] = field(
        default_factory=lambda: [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]
    )


@dataclass
class SafetyAttribute:
    name: str
    score: float
    flagged: bool


@dataclass
class SafetyCheckResponse:
    text: str
    attributes: List[SafetyAttribute]
    overall_safe: bool
    max_score: float = 0.0


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str
    usage_tokens: int = 0


@dataclass
class TranscriptRequest:
    audio_file_path: str
    language_code: str = "en"
    model: str = "assemblyai_default"


@dataclass
class TranscriptResponse:
    text: str
    confidence: float = 0.0
    words: List[Dict[str, Any]] = field(default_factory=list)
    utterances: List[Dict[str, Any]] = field(default_factory=list)
    audio_duration_seconds: float = 0.0


def normalize_voice_info(raw: Dict[str, Any]) -> VoiceInfo:
    return VoiceInfo(
        voice_id=raw.get("voice_id", ""),
        name=raw.get("name", ""),
        category=raw.get("category", ""),
        description=raw.get("description", ""),
        labels=raw.get("labels", {}),
        preview_url=raw.get("preview_url"),
        available_for_tiers=raw.get("available_for_tiers", []),
        settings=raw.get("settings"),
    )


def normalize_translation_response(raw: Dict[str, Any]) -> TranslationResponse:
    translations = raw.get("translations", [])
    if translations:
        t = translations[0]
        return TranslationResponse(
            translated_text=t.get("text", ""),
            source_lang=t.get("detected_source_language", ""),
            target_lang=t.get("target_lang", ""),
        )
    return TranslationResponse(translated_text="", source_lang="", target_lang="")


def normalize_safety_response(
    raw: Dict[str, Any], request_text: str
) -> SafetyCheckResponse:
    attribute_scores = raw.get("attributeScores", {})
    attributes = []
    max_score = 0.0
    for attr_name, attr_data in attribute_scores.items():
        summary = attr_data.get("summaryScore", {})
        score = summary.get("value", 0.0)
        flagged = score > 0.5
        attributes.append(SafetyAttribute(name=attr_name, score=score, flagged=flagged))
        if score > max_score:
            max_score = score
    return SafetyCheckResponse(
        text=request_text,
        attributes=attributes,
        overall_safe=max_score <= 0.5,
        max_score=max_score,
    )


def normalize_embedding_response(raw: Dict[str, Any]) -> EmbeddingResponse:
    data = raw.get("data", [])
    if data:
        item = data[0]
        return EmbeddingResponse(
            embedding=item.get("embedding", []),
            model=item.get("model", ""),
            usage_tokens=raw.get("usage", {}).get("total_tokens", 0),
        )
    return EmbeddingResponse(embedding=[], model="")


def normalize_transcript_response(raw: Dict[str, Any]) -> TranscriptResponse:
    return TranscriptResponse(
        text=raw.get("text", ""),
        confidence=raw.get("confidence", 0.0),
        words=raw.get("words", []),
        utterances=raw.get("utterances", []),
        audio_duration_seconds=raw.get("audio_duration", 0.0) / 1000.0
        if raw.get("audio_duration")
        else 0.0,
    )
