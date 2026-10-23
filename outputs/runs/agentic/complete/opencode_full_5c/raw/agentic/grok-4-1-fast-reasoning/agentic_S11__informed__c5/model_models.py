from typing import TypedDict, List, Any, Generator, Optional, Dict


class ChatMessage(TypedDict):
    role: str
    content: str


class GenerationRequest(TypedDict):
    messages: List[ChatMessage]
    model: str
    max_tokens: Optional[int]
    temperature: Optional[float]


class GenerationResponse(TypedDict):
    content: str
    usage: Optional[Dict[str, Any]]


PlatformStreamResponse = Generator[Any, None, None]
