from typing import List, TypedDict

class ChatMessage(TypedDict):
    role: str
    content: str

class ChatCompletionRequest(TypedDict):
    model: str
    messages: List[ChatMessage]
    stream: bool
    temperature: float

class Usage(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
