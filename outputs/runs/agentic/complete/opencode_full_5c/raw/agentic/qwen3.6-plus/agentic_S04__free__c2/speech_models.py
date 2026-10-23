import os
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum


class TranscriptionStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class AssemblyAIConfig:
    api_key: str = ""
    base_url: str = "https://api.assemblyai.com/v2"
    upload_url: str = "https://api.assemblyai.com/v2/upload"
    timeout: int = 300
    max_retries: int = 3
    retry_delay: float = 5.0

    @classmethod
    def from_env(cls) -> "AssemblyAIConfig":
        return cls(
            api_key=os.getenv("ASSEMBLYAI_API_KEY", ""),
            base_url=os.getenv("ASSEMBLYAI_BASE_URL", "https://api.assemblyai.com/v2"),
            timeout=int(os.getenv("ASSEMBLYAI_TIMEOUT", "300")),
            max_retries=int(os.getenv("ASSEMBLYAI_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("ASSEMBLYAI_RETRY_DELAY", "5.0")),
        )

    def get_headers(self) -> Dict[str, str]:
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
        }


@dataclass
class OpenAIConfig:
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    translation_model: str = "gpt-4o-mini"
    moderation_model: str = "omni-moderation-latest"
    summary_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    timeout: int = 60

    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            translation_model=os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini"),
            moderation_model=os.getenv(
                "OPENAI_MODERATION_MODEL", "omni-moderation-latest"
            ),
            summary_model=os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini"),
            embedding_model=os.getenv(
                "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
            ),
            timeout=int(os.getenv("OPENAI_TIMEOUT", "60")),
        )

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


@dataclass
class TranscriptionRequest:
    audio_url: str = ""
    audio_file_path: str = ""
    speaker_labels: bool = False
    word_timestamps: bool = False
    language_code: Optional[str] = None
    punctuate: bool = True
    format_text: bool = True
    dual_channel: bool = False
    custom_spelling: Optional[List[Dict[str, Any]]] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
        }
        if self.speaker_labels:
            payload["speaker_labels"] = True
        if self.word_timestamps:
            payload["word_timestamps"] = True
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.dual_channel:
            payload["dual_channel"] = True
        if self.custom_spelling:
            payload["custom_spelling"] = self.custom_spelling
        payload.update(self.extra_params)
        return payload


@dataclass
class TranscriptionJob:
    job_id: str = ""
    status: TranscriptionStatus = TranscriptionStatus.QUEUED
    audio_url: str = ""
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None


@dataclass
class WordInfo:
    text: str = ""
    start: int = 0
    end: int = 0
    confidence: float = 0.0
    speaker: Optional[str] = None


@dataclass
class UtteranceInfo:
    text: str = ""
    speaker: Optional[str] = None
    start: int = 0
    end: int = 0
    words: List[WordInfo] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class TranscriptionResult:
    job_id: str = ""
    status: str = ""
    text: str = ""
    words: List[WordInfo] = field(default_factory=list)
    utterances: List[UtteranceInfo] = field(default_factory=list)
    audio_duration: float = 0.0
    language_code: Optional[str] = None
    confidence: float = 0.0

    @classmethod
    def from_assemblyai_response(
        cls, response: Dict[str, Any]
    ) -> "TranscriptionResult":
        words = [
            WordInfo(
                text=w.get("text", ""),
                start=w.get("start", 0),
                end=w.get("end", 0),
                confidence=w.get("confidence", 0.0),
                speaker=w.get("speaker"),
            )
            for w in response.get("words", [])
        ]
        utterances = []
        for u in response.get("utterances", []):
            utterance_words = [
                WordInfo(
                    text=w.get("text", ""),
                    start=w.get("start", 0),
                    end=w.get("end", 0),
                    confidence=w.get("confidence", 0.0),
                    speaker=u.get("speaker"),
                )
                for w in u.get("words", [])
            ]
            utterances.append(
                UtteranceInfo(
                    text=u.get("text", ""),
                    speaker=u.get("speaker"),
                    start=u.get("start", 0),
                    end=u.get("end", 0),
                    words=utterance_words,
                    confidence=u.get("confidence", 0.0),
                )
            )
        return cls(
            job_id=response.get("id", ""),
            status=response.get("status", ""),
            text=response.get("text", ""),
            words=words,
            utterances=utterances,
            audio_duration=response.get("audio_duration", 0.0),
            language_code=response.get("language_code"),
            confidence=response.get("confidence", 0.0),
        )


@dataclass
class TranslationResult:
    segments: List[Dict[str, Any]] = field(default_factory=list)
    target_language: str = ""
    source_language: str = ""

    @classmethod
    def from_openai_response(
        cls, response: Dict[str, Any], target_language: str, source_language: str
    ) -> "TranslationResult":
        choices = response.get("choices", [])
        translated_text = ""
        if choices:
            translated_text = choices[0].get("message", {}).get("content", "")
        segments = []
        try:
            parsed = json.loads(translated_text)
            if isinstance(parsed, list):
                segments = parsed
        except (json.JSONDecodeError, TypeError):
            segments = [{"text": translated_text}]
        return cls(
            segments=segments,
            target_language=target_language,
            source_language=source_language,
        )


@dataclass
class ModerationResult:
    flagged: bool = False
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    sanitized_text: str = ""
    original_text: str = ""

    @classmethod
    def from_openai_response(
        cls, response: Dict[str, Any], original_text: str
    ) -> "ModerationResult":
        results = response.get("results", [])
        if not results:
            return cls(original_text=original_text)
        mod_result = results[0]
        flagged = mod_result.get("flagged", False)
        categories = mod_result.get("categories", {})
        category_scores = mod_result.get("category_scores", {})
        sanitized_text = original_text
        if flagged:
            sanitized_text = "[CONTENT FLAGGED FOR REVIEW]"
        return cls(
            flagged=flagged,
            categories=categories,
            category_scores=category_scores,
            sanitized_text=sanitized_text,
            original_text=original_text,
        )


@dataclass
class SummaryResult:
    summary: str = ""
    key_points: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)

    @classmethod
    def from_openai_response(cls, response: Dict[str, Any]) -> "SummaryResult":
        choices = response.get("choices", [])
        content = ""
        if choices:
            content = choices[0].get("message", {}).get("content", "")
        summary = content
        key_points = []
        topics = []
        action_items = []
        try:
            parsed = json.loads(content)
            summary = parsed.get("summary", content)
            key_points = parsed.get("key_points", [])
            topics = parsed.get("topics", [])
            action_items = parsed.get("action_items", [])
        except (json.JSONDecodeError, TypeError):
            pass
        return cls(
            summary=summary,
            key_points=key_points,
            topics=topics,
            action_items=action_items,
        )


@dataclass
class EmbeddingResult:
    segments: List[Dict[str, Any]] = field(default_factory=list)
    model: str = ""
    total_segments: int = 0

    @classmethod
    def from_openai_response(
        cls, response: Dict[str, Any], segments: List[Dict[str, Any]]
    ) -> "EmbeddingResult":
        data = response.get("data", [])
        model = response.get("model", "")
        enriched_segments = []
        for i, seg in enumerate(segments):
            embedding = None
            if i < len(data):
                embedding = data[i].get("embedding")
            enriched_seg = dict(seg)
            enriched_seg["embedding"] = embedding
            enriched_segments.append(enriched_seg)
        return cls(
            segments=enriched_segments,
            model=model,
            total_segments=len(enriched_segments),
        )
