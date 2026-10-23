from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PlatformInvocationRequest:
    prompt: str
    system_instruction: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 512

    def to_input(self) -> Any:
        if self.system_instruction:
            return [
                {"role": "system", "content": self.system_instruction},
                {"role": "user", "content": self.prompt},
            ]
        return self.prompt


@dataclass
class PlatformInvocationResponse:
    text: str
    provider_response: Any
    model_id: str


@dataclass
class PlatformStreamEvent:
    provider_event: Any


@dataclass
class PlatformStreamResult:
    events: List[PlatformStreamEvent]


@dataclass
class PlatformMetadataResult:
    text: str
    model_id: str
    response_id: Optional[str]
    usage: Any
    provider_response: Any


def normalize_text_response(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text
    output = getattr(response, "output", None)
    if isinstance(output, list):
        pieces = []
        for item in output:
            content = getattr(item, "content", None) or item.get("content") if isinstance(item, dict) else None
            if isinstance(content, list):
                for part in content:
                    t = getattr(part, "text", None) if not isinstance(part, dict) else part.get("text")
                    if t:
                        pieces.append(t)
        if pieces:
            return "".join(pieces)
    return str(response)
