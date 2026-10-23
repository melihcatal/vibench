from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class ModelRequest:
    prompt: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    # Add other common request parameters as needed

@dataclass
class ModelResponse:
    text: str
    metadata: Dict[str, Any]

@dataclass
class SafetyResult:
    is_safe: bool
    categories: Dict[str, float]
    details: Optional[str] = None

@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: str

@dataclass
class EmbeddingResult:
    embedding: List[float]
    text: str
    model_id: str

@dataclass
class AudioBriefingResult:
    audio_content: bytes
    format: str
    text_processed: str

def normalize_vertex_ai_response(vertex_response: Any) -> ModelResponse:
    """Normalizes a Vertex AI response object."""
    text_content = vertex_response.text
    # Vertex AI response objects might contain detailed metadata if accessed via
    # `_raw_response` or specific attributes. For simplicity, we'll keep it minimal.
    metadata = {
        "provider": "Vertex AI",
        # "usage_metadata": vertex_response.usage_metadata # Example, if available
    }
    return ModelResponse(text=text_content, metadata=metadata)

def normalize_azure_openai_response(azure_response: Any) -> ModelResponse:
    """Normalizes an Azure OpenAI response object."""
    text_content = azure_response.choices[0].message.content
    metadata = {
        "provider": "Azure OpenAI",
        "model": azure_response.model,
        "completion_tokens": azure_response.usage.completion_tokens,
        "prompt_tokens": azure_response.usage.prompt_tokens,
        "total_tokens": azure_response.usage.total_tokens,
    }
    return ModelResponse(text=text_content, metadata=metadata)

def normalize_bedrock_response_chunk(chunk_obj: Dict[str, Any]) -> str:
    """Normalizes a Bedrock streaming chunk object to text."""
    return chunk_obj.get('completion', '')

def normalize_huggingface_response(hf_text_response: str, model_id: str) -> ModelResponse:
    """Normalizes a Hugging Face text generation response."""
    metadata = {
        "provider": "Hugging Face Inference API",
        "model_id": model_id,
        "response_length": len(hf_text_response),
    }
    return ModelResponse(text=hf_text_response, metadata=metadata)

