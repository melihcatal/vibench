import dataclasses

@dataclasses.dataclass
class LLMRequest:
    prompt: str
    model: str = "gemini-pro"
    temperature: float = 0.7

@dataclasses.dataclass
class LLMResponse:
    text: str
    finish_reason: str = "STOP"

@dataclasses.dataclass
class EmbeddingRequest:
    text: str
    model: str = "models/embedding-001"

@dataclasses.dataclass
class EmbeddingResponse:
    embedding: list[float]
