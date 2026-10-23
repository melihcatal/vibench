from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ChatMessage:
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

@dataclass
class ChatRequest:
    messages: List[ChatMessage]
    model: str = "gpt-4o"
    max_tokens: int = 1024
    temperature: float = 0.7

    def to_api_payload(self) -> Dict:
        return {
            "model": self.model,
            "messages": [m.to_dict() for m in self.messages],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
