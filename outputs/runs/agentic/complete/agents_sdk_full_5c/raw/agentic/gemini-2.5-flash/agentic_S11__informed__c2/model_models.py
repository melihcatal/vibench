from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class ModelInvocationRequest:
    prompt: str
    model_id: str
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None

@dataclass
class ModelInvocationResponse:
    text_output: str
    finish_reason: Optional[str] = None
    prompt_token_count: Optional[int] = None
    
    @classmethod
    def from_vertexai_response(cls, response: Any):
        """Normalizes a Vertex AI GenerativeModel response into ModelInvocationResponse."""
        text_output = response.text if response.text else ""
        finish_reason = response.candidates[0].finish_reason.name if response.candidates and hasattr(response.candidates[0], 'finish_reason') else None
        prompt_token_count = response.usage_metadata.prompt_token_count if response.usage_metadata and hasattr(response.usage_metadata, 'prompt_token_count') else None
        
        return cls(
            text_output=text_output,
            finish_reason=finish_reason,
            prompt_token_count=prompt_token_count
        )

@dataclass
class SafetyCheckResult:
    is_safe: bool
    categories: Optional[Dict[str, float]] = None
    details: Optional[Any] = None

@dataclass
class TranslationResult:
    translated_text: str
    source_language_code: Optional[str] = None
    target_language_code: Optional[str] = None

@dataclass
class EmbeddingResult:
    embedding: list[float]
    token_count: Optional[int] = None

@dataclass
class AudioBriefingResult:
    audio_content: bytes
    mime_type: str
