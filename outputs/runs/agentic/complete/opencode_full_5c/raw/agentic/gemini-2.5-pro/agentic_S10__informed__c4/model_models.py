from dataclasses import dataclass


@dataclass
class CompletionRequest:
    prompt: str
    model: str = "gpt-4o"
    max_tokens: int = 1024
    temperature: float = 0.7


@dataclass
class CompletionResponse:
    text: str


@dataclass
class StreamChunk:
    text: str
