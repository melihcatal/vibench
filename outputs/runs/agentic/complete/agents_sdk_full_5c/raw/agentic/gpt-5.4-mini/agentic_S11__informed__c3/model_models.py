from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.2


@dataclass
class PlatformResponse:
    text: str
    model_id: str
    usage: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None



def normalize_text_response(payload: Dict[str, Any]) -> PlatformResponse:
    text = ""
    if "outputText" in payload:
        text = payload["outputText"]
    elif "results" in payload and payload["results"]:
        first = payload["results"][0]
        text = first.get("outputText", first.get("text", ""))
    elif "content" in payload:
        content = payload["content"]
        if isinstance(content, list) and content:
            text = content[0].get("text", "")
    return PlatformResponse(
        text=text,
        model_id=payload.get("modelId", payload.get("model_id", "amazon-bedrock")),
        usage=payload.get("usage"),
        metadata=payload,
    )



def build_converse_messages(prompt: str) -> List[Dict[str, Any]]:
    return [{"role": "user", "content": [{"text": prompt}]}]



def serialize_prompt(prompt: str, max_tokens: int, temperature: float) -> str:
    return json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": build_converse_messages(prompt),
        }
    )
