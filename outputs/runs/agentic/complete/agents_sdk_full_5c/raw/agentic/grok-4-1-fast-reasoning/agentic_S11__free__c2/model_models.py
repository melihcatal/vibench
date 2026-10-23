from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ChatMessage(BaseModel):
    role: str
    content: str

class CompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: Optional[int] = None

def normalize_request(prompt: str, model: str, **kwargs) -> Dict[str, Any]:
    return {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        **kwargs
    }