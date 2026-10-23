from typing import List, Dict, Any, Optional

class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

class CompletionRequest:
    def __init__(self, messages: List[ChatMessage], model: str = "gpt-4o", temperature: float = 0.7, max_tokens: int = 150):
        self.messages = messages
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "messages": [msg.to_dict() for msg in self.messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

class CompletionResponse:
    def __init__(self, content: str, model: str):
        self.content = content
        self.model = model

class StreamChunk:
    def __init__(self, delta_content: Optional[str] = None):
        self.delta_content = delta_content
