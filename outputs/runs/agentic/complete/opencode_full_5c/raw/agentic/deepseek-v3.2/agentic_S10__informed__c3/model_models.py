from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import json


@dataclass
class ChatMessage:
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class CompletionRequest:
    messages: List[ChatMessage]
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: Optional[int] = None

    def to_openai_format(self) -> Dict[str, Any]:
        result = {
            "model": self.model,
            "messages": [msg.to_dict() for msg in self.messages],
            "temperature": self.temperature,
        }
        if self.max_tokens:
            result["max_tokens"] = self.max_tokens
        return result


@dataclass
class CompletionResponse:
    content: str
    model: str
    usage: Optional[Dict[str, int]] = None

    @classmethod
    def from_openai_response(cls, response) -> "CompletionResponse":
        content = response.choices[0].message.content
        model = response.model
        usage = (
            {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
            if response.usage
            else None
        )
        return cls(content=content, model=model, usage=usage)


@dataclass
class StreamChunk:
    content: str
    done: bool = False

    @classmethod
    def from_openai_chunk(cls, chunk) -> "StreamChunk":
        if chunk.choices[0].finish_reason is not None:
            return cls(content="", done=True)

        delta = chunk.choices[0].delta
        content = delta.content if delta.content else ""
        return cls(content=content, done=False)


def normalize_text(text: str) -> str:
    return text.strip()


def parse_json_response(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())
