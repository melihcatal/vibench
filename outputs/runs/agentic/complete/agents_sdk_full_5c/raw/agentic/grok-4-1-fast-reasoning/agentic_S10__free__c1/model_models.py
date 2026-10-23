from typing import TypedDict, List, Dict, Any, Optional, Generator

class Message(TypedDict):
    role: str
    content: str

class ChatCompletionRequest(TypedDict):
    model: str
    messages: List[Message]
    temperature: Optional[float]
    max_tokens: Optional[int]
    stream: bool

class ChatCompletionResponse(TypedDict):
    choices: List[Dict[str, Any]] 

class ModerationResult(TypedDict):
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
