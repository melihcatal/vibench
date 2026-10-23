from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class ModelFamily(Enum):
    """Enumeration of model families."""

    GPT = "gpt"
    CLAUDE = "claude"
    MISTRAL = "mistral"
    GEMINI = "gemini"
    LLAMA = "llama"
    QWEN = "qwen"


@dataclass
class CompletionRequest:
    """Request for model completion."""

    prompt: str
    model: str
    max_tokens: int = 100
    temperature: float = 0.7
    system_prompt: Optional[str] = None
    stream: bool = False

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})

        return {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": self.stream,
        }

    def to_anthropic_format(self) -> Dict[str, Any]:
        """Convert to Anthropic API format."""
        messages = [{"role": "user", "content": self.prompt}]

        return {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }


@dataclass
class CompletionResponse:
    """Response from model completion."""

    content: str
    model: str
    usage: Optional[Dict[str, int]] = None
    finish_reason: Optional[str] = None

    @classmethod
    def from_openai(cls, openai_response: Any) -> "CompletionResponse":
        """Create from OpenAI response."""
        return cls(
            content=openai_response.choices[0].message.content,
            model=openai_response.model,
            usage={
                "prompt_tokens": openai_response.usage.prompt_tokens,
                "completion_tokens": openai_response.usage.completion_tokens,
                "total_tokens": openai_response.usage.total_tokens,
            }
            if openai_response.usage
            else None,
            finish_reason=openai_response.choices[0].finish_reason,
        )

    @classmethod
    def from_anthropic(cls, anthropic_response: Any) -> "CompletionResponse":
        """Create from Anthropic response."""
        return cls(
            content=anthropic_response.content[0].text,
            model=anthropic_response.model,
            usage={
                "input_tokens": anthropic_response.usage.input_tokens,
                "output_tokens": anthropic_response.usage.output_tokens,
            }
            if hasattr(anthropic_response, "usage")
            else None,
        )


def normalize_model_name(model_name: str) -> str:
    """Normalize model name for consistent comparison."""
    model_name = model_name.lower()

    # Map common variations
    variations = {
        "gpt-3.5": "gpt-3.5-turbo",
        "gpt-4": "gpt-4-turbo",
        "claude-3": "claude-3-haiku",
        "mistral-small": "mistral-small-latest",
    }

    for variant, normalized in variations.items():
        if variant in model_name:
            return normalized

    return model_name


def detect_model_family(model_name: str) -> ModelFamily:
    """Detect the model family from model name."""
    model_name = model_name.lower()

    if "gpt" in model_name:
        return ModelFamily.GPT
    elif "claude" in model_name:
        return ModelFamily.CLAUDE
    elif "mistral" in model_name:
        return ModelFamily.MISTRAL
    elif "gemini" in model_name:
        return ModelFamily.GEMINI
    elif "llama" in model_name:
        return ModelFamily.LLAMA
    elif "qwen" in model_name:
        return ModelFamily.QWEN
    else:
        return ModelFamily.GPT  # Default


def get_model_capabilities(model_family: ModelFamily) -> Dict[str, Any]:
    """Get capabilities for a model family."""
    capabilities = {
        ModelFamily.GPT: {
            "max_context": 16385,
            "supports_json_mode": True,
            "supports_function_calling": True,
            "supports_vision": True,
        },
        ModelFamily.CLAUDE: {
            "max_context": 200000,
            "supports_json_mode": False,
            "supports_function_calling": False,
            "supports_vision": True,
        },
        ModelFamily.MISTRAL: {
            "max_context": 32768,
            "supports_json_mode": True,
            "supports_function_calling": True,
            "supports_vision": False,
        },
    }
    return capabilities.get(model_family, {})
