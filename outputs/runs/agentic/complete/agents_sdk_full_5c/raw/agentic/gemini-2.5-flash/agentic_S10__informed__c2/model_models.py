
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class LLMRequest:
    prompt: str
    model_name: str = "gemini-pro"
    max_output_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    stop_sequences: Optional[List[str]] = None
    system_instruction: Optional[str] = None
    context: Optional[str] = None

@dataclass
class LLMResponse:
    text: str
    finish_reason: Optional[str] = None
    token_count: Optional[Dict[str, Any]] = None

@dataclass
class StructuredExtractionResponse:
    json_data: Optional[Dict[str, Any]] = None
    raw_text: str

@dataclass
class SafetyCheckRequest:
    text_content: str
    categories: List[str] = field(default_factory=lambda: ["Hate", "SelfHarm", "Sexual", "Violence"])

@dataclass
class SafetyCheckResponse:
    is_safe: bool
    moderation_results: Dict[str, Any]

@dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language_code: Optional[str] = None

@dataclass
class EmbeddingRequest:
    text_content: List[str]
    model_name: str = "models/embedding-001"

@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]

@dataclass
class TextToSpeechRequest:
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Standard-A"
    audio_encoding: str = "MP3" # LINEAR16, MP3, OGG_OPUS

@dataclass
class TextToSpeechResponse:
    audio_content: bytes
