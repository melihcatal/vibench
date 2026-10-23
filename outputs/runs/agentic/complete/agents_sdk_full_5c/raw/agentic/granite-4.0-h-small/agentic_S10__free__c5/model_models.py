from typing import TypedDict, Literal, Any

class LLMRequest(TypedDict):
    model: str
    messages: list[dict[str, str]]
    temperature: float

LLMResponse = TypedDict('LLMResponse', {
    'choices': list[dict[str, Any]]
]}

ParsedLLMResponse = TypedDict('ParsedLLMResponse', {
    'content': str
])
