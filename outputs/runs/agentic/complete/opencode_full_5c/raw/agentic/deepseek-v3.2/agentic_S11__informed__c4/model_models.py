from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import json


@dataclass
class ModelRequest:
    prompt: str
    model_id: str = "ibm/granite-13b-chat-v2"
    parameters: Optional[Dict[str, Any]] = None
    stream: bool = False

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "prompt": self.prompt,
            "model_id": self.model_id,
            "stream": self.stream,
        }
        if self.parameters:
            result["parameters"] = self.parameters
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class ModelResponse:
    text: str
    model_id: str
    request_id: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"text": self.text, "model_id": self.model_id}
        if self.request_id:
            result["request_id"] = self.request_id
        if self.usage:
            result["usage"] = self.usage
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class ModelMetadata:
    provider: str = "IBM watsonx.ai"
    project_id: Optional[str] = None
    api_endpoint: Optional[str] = None
    model_family: Optional[str] = None
    parameters_used: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_watsonx_response(response) -> ModelResponse:
    text = ""
    model_id = ""
    request_id = None
    usage = None

    if hasattr(response, "choices") and response.choices:
        text = response.choices[0].text
    elif hasattr(response, "generated_text"):
        text = response.generated_text

    if hasattr(response, "model_id"):
        model_id = response.model_id

    if hasattr(response, "id"):
        request_id = response.id

    if hasattr(response, "usage"):
        usage = {
            "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
            "completion_tokens": getattr(response.usage, "completion_tokens", 0),
            "total_tokens": getattr(response.usage, "total_tokens", 0),
        }

    return ModelResponse(
        text=text, model_id=model_id, request_id=request_id, usage=usage
    )


def create_chat_prompt(messages: List[Dict[str, str]]) -> str:
    prompt_parts = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "system":
            prompt_parts.append(f"System: {content}")
        elif role == "user":
            prompt_parts.append(f"User: {content}")
        elif role == "assistant":
            prompt_parts.append(f"Assistant: {content}")

    prompt_parts.append("Assistant:")
    return "\n".join(prompt_parts)
