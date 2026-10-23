from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class GenerationRequest:
    prompt: str
    system: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 300
    locale: str = "en"


@dataclass
class ResourceSelection:
    inference_profile_arn: str
    model_id: str
    region_name: str
    provider: str = "aws_bedrock"
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class GenerationResult:
    text: str
    model_id: str
    resource_id: str
    usage: Dict[str, Any]
    raw: Dict[str, Any]


def build_messages(request: GenerationRequest) -> List[Dict[str, Any]]:
    content: List[Dict[str, Any]] = [{"text": request.prompt}]
    return [{"role": "user", "content": content}]


def build_system_prompts(request: GenerationRequest) -> List[Dict[str, str]]:
    if not request.system:
        return []
    return [{"text": request.system}]


def coalesce_text_blocks(blocks: Iterable[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for block in blocks:
        text = block.get("text")
        if text:
            parts.append(text)
    return "".join(parts)


def normalize_bedrock_converse_response(
    response: Dict[str, Any], model_id: str, resource_id: str
) -> GenerationResult:
    output = response.get("output", {})
    message = output.get("message", {})
    content = message.get("content", [])
    usage = response.get("usage", {})
    return GenerationResult(
        text=coalesce_text_blocks(content),
        model_id=model_id,
        resource_id=resource_id,
        usage=usage,
        raw=response,
    )
