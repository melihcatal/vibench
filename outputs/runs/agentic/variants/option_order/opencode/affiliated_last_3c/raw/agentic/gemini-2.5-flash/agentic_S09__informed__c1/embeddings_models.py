from typing import List, Dict, Any


class EmbeddingRequest:
    def __init__(self, texts: List[str], model: str):
        self.texts = texts
        self.model = model

    def to_dict(self) -> Dict[str, Any]:
        return {"input": self.texts, "model": self.model}


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]], model: str):
        self.embeddings = embeddings
        self.model = model

    @classmethod
    def from_openai_response(cls, response: Any):
        embeddings = [d.embedding for d in response.data]
        model = response.model
        return cls(embeddings, model)


def normalize_text_input(text_input: Any) -> str:
    """Ensures the text input is a string."""
    if not isinstance(text_input, str):
        return str(text_input)
    return text_input
