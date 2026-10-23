from typing import List, Dict, Any, Optional

class EmbeddingRequest:
    text: str
    model_name: str

    def __init__(self, text: str, model_name: str):
        self.text = text
        self.model_name = model_name

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "model_name": self.model_name}

class EmbeddingResponse:
    embedding: List[float]
    model_name: str
    input_text: str

    def __init__(self, embedding: List[float], model_name: str, input_text: str):
        self.embedding = embedding
        self.model_name = model_name
        self.input_text = input_text

    def to_dict(self) -> Dict[str, Any]:
        return {"embedding": self.embedding, "model_name": self.model_name, "input_text": self.input_text}

class BatchEmbeddingRequest:
    texts: List[str]
    model_name: str

    def __init__(self, texts: List[str], model_name: str):
        self.texts = texts
        self.model_name = model_name

    def to_dict(self) -> Dict[str, Any]:
        return {"texts": self.texts, "model_name": self.model_name}

class BatchEmbeddingResponse:
    embeddings: List[List[float]]
    model_name: str
    input_texts: List[str]

    def __init__(self, embeddings: List[List[float]], model_name: str, input_texts: List[str]):
        self.embeddings = embeddings
        self.model_name = model_name
        self.input_texts = input_texts

    def to_dict(self) -> Dict[str, Any]:
        return {"embeddings": self.embeddings, "model_name": self.model_name, "input_texts": self.input_texts}

class SimilarityScoreRequest:
    embedding1: List[float]
    embedding2: List[float]

    def __init__(self, embedding1: List[float], embedding2: List[float]):
        self.embedding1 = embedding1
        self.embedding2 = embedding2

    def to_dict(self) -> Dict[str, Any]:
        return {"embedding1": self.embedding1, "embedding2": self.embedding2}

class SimilarityScoreResponse:
    score: float
    method: str = "cosine_similarity"

    def __init__(self, score: float, method: str = "cosine_similarity"):
        self.score = score
        self.method = method

    def to_dict(self) -> Dict[str, Any]:
        return {"score": self.score, "method": self.method}

def normalize_embedding_input(text_or_texts: Any) -> List[str]:
    """
    Ensures input for embedding is a list of strings.
    """
    if isinstance(text_or_texts, str):
        return [text_or_texts]
    elif isinstance(text_or_texts, list):
        if all(isinstance(t, str) for t in text_or_texts):
            return text_or_texts
    raise TypeError("Input must be a string or a list of strings.")
