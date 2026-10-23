from dataclasses import dataclass

@dataclass
class LLMRequest:
    prompt: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 150
    temperature: float = 0.7

@dataclass
class LLMResponse:
    text: str
    model_id: str
    finish_reason: str
