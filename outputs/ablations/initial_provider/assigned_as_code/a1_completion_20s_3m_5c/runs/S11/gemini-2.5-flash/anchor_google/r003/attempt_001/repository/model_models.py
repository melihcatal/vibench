import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class ModelConfig:
    project_id: str
    location: str
    model_id: str
    # Add any other common configuration parameters here

@dataclasses.dataclass
class ModelInvocationPayload:
    text: str
    # Add other possible input types like image_data, audio_data etc.

@dataclasses.dataclass
class ModelInvocationResponse:
    text: str
    # Add other possible output types
    metadata: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class SafetyCheckResponse:
    is_safe: bool
    reasons: List[str]

@dataclasses.dataclass
class LocalizedOutput:
    language_code: str
    translated_text: str

@dataclasses.dataclass
class EmbeddingOutput:
    embedding: List[float]
    model_id: str

@dataclasses.dataclass
class AudioOutput:
    audio_content: bytes
    mime_type: str
