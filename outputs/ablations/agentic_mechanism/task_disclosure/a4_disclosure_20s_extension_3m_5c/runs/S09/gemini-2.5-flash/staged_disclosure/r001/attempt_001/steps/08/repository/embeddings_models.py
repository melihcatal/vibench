
# embeddings_models.py

class EmbeddingsRequest:
    def __init__(self, texts: list[str], model: str):
        self.texts = texts
        self.model = model

    def to_dict(self):
        return {
            "input": self.texts,
            "model": self.model
        }

class Embedding:
    def __init__(self, value: list[float], index: int):
        self.value = value
        self.index = index

class EmbeddingsResponse:
    def __init__(self, data: list[dict], model: str):
        self.embeddings = [Embedding(value=item["embedding"], index=item["index"]) for item in data]
        self.model = model

    @classmethod
    def from_dict(cls, response_dict: dict):
        return cls(
            data=response_dict["data"],
            model=response_dict["model"]
        )

def normalize_embeddings_response(response: EmbeddingsResponse) -> list[list[float]]:
    """
    Normalizes the EmbeddingsResponse object into a list of embedding vectors.
    """
    sorted_embeddings = sorted(response.embeddings, key=lambda x: x.index)
    return [embedding.value for embedding in sorted_embeddings]
