from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class ModelRequest:
    """Standardized model request structure."""

    prompt: str
    system_instruction: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 1024
    top_p: float = 0.95
    top_k: int = 40
    stop_sequences: List[str] = None
    deployment_name: str = "text-bison"

    def to_vertex_format(self) -> Dict[str, Any]:
        """Convert to Vertex AI format."""
        instances = []

        if self.system_instruction:
            instances.append(
                {
                    "messages": [
                        {"author": "system", "content": self.system_instruction},
                        {"author": "user", "content": self.prompt},
                    ]
                }
            )
        else:
            instances.append({"content": self.prompt})

        parameters = {
            "temperature": self.temperature,
            "maxOutputTokens": self.max_tokens,
            "topP": self.top_p,
            "topK": self.top_k,
        }

        if self.stop_sequences:
            parameters["stopSequences"] = self.stop_sequences

        return {"instances": instances, "parameters": parameters}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "prompt": self.prompt,
            "system_instruction": self.system_instruction,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "stop_sequences": self.stop_sequences,
            "deployment_name": self.deployment_name,
        }


@dataclass
class ModelResponse:
    """Standardized model response structure."""

    content: str
    request_id: Optional[str] = None
    model_deployment: str = "text-bison"
    usage: Optional[Dict[str, int]] = None
    metadata: Optional[Dict[str, Any]] = None
    latency_ms: Optional[int] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    @classmethod
    def from_vertex_response(
        cls, vertex_response, request: ModelRequest, latency_ms: int
    ) -> "ModelResponse":
        """Create from Vertex AI response."""
        content = ""
        usage = {}
        metadata = {}

        if hasattr(vertex_response, "predictions") and vertex_response.predictions:
            if len(vertex_response.predictions) > 0:
                pred = vertex_response.predictions[0]
                if isinstance(pred, dict) and "content" in pred:
                    content = pred["content"]
                elif hasattr(pred, "content"):
                    content = pred.content
                else:
                    content = str(pred)

        if hasattr(vertex_response, "metadata"):
            metadata = vertex_response.metadata
            if isinstance(metadata, dict):
                if "tokenMetadata" in metadata:
                    token_meta = metadata["tokenMetadata"]
                    if "inputTokenCount" in token_meta:
                        usage["input_tokens"] = token_meta["inputTokenCount"].get(
                            "totalTokens", 0
                        )
                    if "outputTokenCount" in token_meta:
                        usage["output_tokens"] = token_meta["outputTokenCount"].get(
                            "totalTokens", 0
                        )
                elif "usageMetadata" in metadata:
                    usage_meta = metadata["usageMetadata"]
                    usage["input_tokens"] = usage_meta.get("promptTokenCount", 0)
                    usage["output_tokens"] = usage_meta.get("candidatesTokenCount", 0)
                    usage["total_tokens"] = usage_meta.get("totalTokenCount", 0)

        request_id = None
        if hasattr(vertex_response, "request_id"):
            request_id = vertex_response.request_id

        return cls(
            content=content,
            request_id=request_id,
            model_deployment=request.deployment_name,
            usage=usage,
            metadata=metadata,
            latency_ms=latency_ms,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "request_id": self.request_id,
            "model_deployment": self.model_deployment,
            "usage": self.usage,
            "metadata": self.metadata,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class StreamingChunk:
    """Streaming response chunk."""

    content: str
    chunk_index: int
    is_complete: bool = False
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "chunk_index": self.chunk_index,
            "is_complete": self.is_complete,
            "metadata": self.metadata,
        }


def normalize_prompt(prompt: Any) -> str:
    """Normalize prompt input to string."""
    if isinstance(prompt, str):
        return prompt.strip()
    elif isinstance(prompt, dict):
        if "content" in prompt:
            return str(prompt["content"]).strip()
        elif "text" in prompt:
            return str(prompt["text"]).strip()
        elif "prompt" in prompt:
            return str(prompt["prompt"]).strip()
    return str(prompt).strip()


def validate_request(request: Dict[str, Any]) -> List[str]:
    """Validate request parameters and return list of errors."""
    errors = []

    if "prompt" not in request:
        errors.append("Missing required field: prompt")
    elif not request["prompt"] or not str(request["prompt"]).strip():
        errors.append("Prompt cannot be empty")

    if "temperature" in request:
        temp = request["temperature"]
        if not isinstance(temp, (int, float)):
            errors.append("Temperature must be a number")
        elif temp < 0 or temp > 1:
            errors.append("Temperature must be between 0 and 1")

    if "max_tokens" in request:
        max_tokens = request["max_tokens"]
        if not isinstance(max_tokens, int):
            errors.append("max_tokens must be an integer")
        elif max_tokens < 1 or max_tokens > 8192:
            errors.append("max_tokens must be between 1 and 8192")

    return errors


def merge_responses(responses: List[ModelResponse]) -> ModelResponse:
    """Merge multiple responses into one."""
    if not responses:
        return ModelResponse(content="")

    merged_content = " ".join([r.content for r in responses])

    total_input_tokens = sum(
        r.usage.get("input_tokens", 0) for r in responses if r.usage
    )
    total_output_tokens = sum(
        r.usage.get("output_tokens", 0) for r in responses if r.usage
    )

    usage = {
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
    }

    return ModelResponse(
        content=merged_content,
        model_deployment=responses[0].model_deployment,
        usage=usage,
        timestamp=responses[0].timestamp,
    )
