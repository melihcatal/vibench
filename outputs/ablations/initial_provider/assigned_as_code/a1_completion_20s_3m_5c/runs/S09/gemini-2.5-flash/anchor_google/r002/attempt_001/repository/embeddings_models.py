from typing import List, Dict, Union

class EmbeddingRequest:
    def __init__(self, texts: Union[str, List[str]], model: str = "models/embedding-001"):
        self.texts = texts
        self.model = model

    def to_genai_content(self):
        if isinstance(self.texts, str):
            return [self.texts]
        return self.texts

class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]], model: str = "models/embedding-001"):
        self.embeddings = embeddings
        self.model = model

    @classmethod
    def from_genai_response(cls, genai_response, model: str = "models/embedding-001"):
        embeddings = []
        for embedding_obj in genai_response.embeddings:
            # The SDK returns a dictionary-like object for each embedding
            # We need to extract the 'values' which is the actual list of floats
            embeddings.append(list(embedding_obj.values))
        return cls(embeddings=embeddings, model=model)

