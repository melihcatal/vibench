from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class PromptInput:
    text: str
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ModelOutput:
    generated_text: str
    safety_attributes: Optional[Dict[str, Any]] = None
    usage_metadata: Optional[Dict[str, Any]] = None
    raw_response: Optional[Any] = None # To hold the original provider response object

@dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class TranslationOutput:
    translated_text: str
    detected_source_language_code: Optional[str] = None
    raw_response: Optional[Any] = None

@dataclass
class EmbeddingInput:
    text: List[str]

@dataclass
class EmbeddingOutput:
    embeddings: List[List[float]]
    raw_response: Optional[Any] = None

@dataclass
class AudioBriefingInput:
    text: str
    voice_name: str = "en-US-Standard-C"
    audio_format: str = "MP3"

@dataclass
class AudioBriefingOutput:
    audio_content: bytes
    raw_response: Optional[Any] = None
