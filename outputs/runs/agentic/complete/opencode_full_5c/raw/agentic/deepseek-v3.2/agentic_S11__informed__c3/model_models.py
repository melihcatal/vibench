from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum
import json


class ModelProvider(Enum):
    """Enumeration of model providers."""

    ANTHROPIC = "anthropic"
    META = "meta"
    AMAZON = "amazon"
    AI21 = "ai21"
    COHERE = "cohere"
    STABILITY = "stability"


class ModelModality(Enum):
    """Enumeration of model modalities."""

    TEXT = "TEXT"
    IMAGE = "IMAGE"
    EMBEDDING = "EMBEDDING"
    MULTIMODAL = "MULTIMODAL"


@dataclass
class ModelRequest:
    """Base request model for model invocations."""

    prompt: str
    model_id: str
    max_tokens: int = 1000
    temperature: float = 0.7
    system_prompt: Optional[str] = None
    stop_sequences: List[str] = field(default_factory=list)
    additional_params: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        base = {
            "prompt": self.prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

        if self.system_prompt:
            base["system"] = self.system_prompt

        if self.stop_sequences:
            base["stop_sequences"] = self.stop_sequences

        base.update(self.additional_params)
        return base

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class ModelResponse:
    """Base response model for model outputs."""

    text: str
    model_id: str
    request_id: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    stop_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def input_tokens(self) -> int:
        """Get input token count from usage."""
        if self.usage:
            return self.usage.get("input_tokens", 0)
        return 0

    @property
    def output_tokens(self) -> int:
        """Get output token count from usage."""
        if self.usage:
            return self.usage.get("output_tokens", 0)
        return 0

    @property
    def total_tokens(self) -> int:
        """Get total token count from usage."""
        if self.usage:
            return self.usage.get("total_tokens", 0)
        return self.input_tokens + self.output_tokens

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "text": self.text,
            "model_id": self.model_id,
            "request_id": self.request_id,
            "usage": self.usage,
            "stop_reason": self.stop_reason,
            "metadata": self.metadata,
            "token_counts": {
                "input": self.input_tokens,
                "output": self.output_tokens,
                "total": self.total_tokens,
            },
        }


@dataclass
class StreamChunk:
    """Chunk of streamed response."""

    text: str
    chunk_index: int
    is_complete: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelInfo:
    """Information about a specific model."""

    model_id: str
    model_name: str
    provider: ModelProvider
    modalities: List[ModelModality]
    max_tokens: int
    supported_customizations: List[str] = field(default_factory=list)
    inference_types: List[str] = field(default_factory=list)

    @classmethod
    def from_bedrock_summary(cls, summary: Dict[str, Any]) -> "ModelInfo":
        """Create from Amazon Bedrock model summary."""
        provider_name = summary.get("providerName", "").lower()
        if "anthropic" in provider_name:
            provider = ModelProvider.ANTHROPIC
        elif "meta" in provider_name:
            provider = ModelProvider.META
        elif "amazon" in provider_name:
            provider = ModelProvider.AMAZON
        elif "ai21" in provider_name:
            provider = ModelProvider.AI21
        elif "cohere" in provider_name:
            provider = ModelProvider.COHERE
        elif "stability" in provider_name:
            provider = ModelProvider.STABILITY
        else:
            provider = ModelProvider.AMAZON

        modalities = []
        input_mods = summary.get("inputModalities", [])
        output_mods = summary.get("outputModalities", [])
        all_mods = input_mods + output_mods

        for mod in all_mods:
            try:
                modalities.append(ModelModality(mod))
            except ValueError:
                pass

        return cls(
            model_id=summary.get("modelId", ""),
            model_name=summary.get("modelName", ""),
            provider=provider,
            modalities=modalities,
            max_tokens=summary.get("maxTokens", 4096),
            supported_customizations=summary.get("customizationsSupported", []),
            inference_types=summary.get("inferenceTypesSupported", []),
        )


class ResponseNormalizer:
    """Utility for normalizing responses from different providers."""

    @staticmethod
    def normalize_bedrock_response(
        model_id: str, response_body: Dict[str, Any]
    ) -> ModelResponse:
        """Normalize Bedrock response to standard format."""
        if "anthropic" in model_id:
            text = response_body["content"][0]["text"]
            usage = response_body.get("usage", {})
            stop_reason = response_body.get("stop_reason")
        elif "meta" in model_id:
            text = response_body["generation"]
            usage = {
                "input_tokens": response_body.get("prompt_token_count", 0),
                "output_tokens": response_body.get("generation_token_count", 0),
                "total_tokens": (
                    response_body.get("prompt_token_count", 0)
                    + response_body.get("generation_token_count", 0)
                ),
            }
            stop_reason = response_body.get("stop_reason")
        elif "amazon" in model_id:
            text = response_body["results"][0]["outputText"]
            usage = {
                "input_tokens": response_body.get("inputTextTokenCount", 0),
                "output_tokens": len(response_body["results"][0]["outputText"].split()),
                "total_tokens": response_body.get("inputTextTokenCount", 0)
                + len(response_body["results"][0]["outputText"].split()),
            }
            stop_reason = response_body["results"][0].get("completionReason")
        else:
            text = response_body.get(
                "completion", response_body.get("generated_text", "")
            )
            usage = {}
            stop_reason = None

        return ModelResponse(
            text=text,
            model_id=model_id,
            usage=usage,
            stop_reason=stop_reason,
            metadata={"raw_response": response_body},
        )

    @staticmethod
    def normalize_stream_chunk(
        model_id: str, chunk_data: Dict[str, Any]
    ) -> StreamChunk:
        """Normalize stream chunk from different providers."""
        if "anthropic" in model_id:
            if "delta" in chunk_data:
                text = chunk_data["delta"].get("text", "")
                return StreamChunk(text=text, chunk_index=0)
            elif "message" in chunk_data:
                return StreamChunk(
                    text="", chunk_index=0, metadata={"message": chunk_data["message"]}
                )
        elif "meta" in model_id:
            if "generation" in chunk_data:
                text = chunk_data["generation"]
                return StreamChunk(text=text, chunk_index=0)
        elif "amazon" in model_id:
            if "outputText" in chunk_data:
                text = chunk_data["outputText"]
                return StreamChunk(text=text, chunk_index=0)
        else:
            if "completion" in chunk_data:
                text = chunk_data["completion"]
                return StreamChunk(text=text, chunk_index=0)

        return StreamChunk(text="", chunk_index=0)
