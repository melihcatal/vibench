from typing import List, Dict, Union

class EmbeddingRequest:
    def __init__(self, texts: Union[str, List[str]], model: str = "gemini-embedding-001"):
        self.texts = texts
        self.model = model

    def to_client_payload(self) -> List[str]:
        if isinstance(self.texts, str):
            return [self.texts]
        return self.texts

class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings

    @classmethod
    def from_client_response(cls, client_response: List[List[float]]) -> 'EmbeddingResponse':
        return cls(embeddings=client_response)

    def to_dict(self) -> Dict[str, List[List[float]]]:
        return {"embeddings": self.embeddings}

class SimilarityScoreRequest:
    def __init__(self, embedding1: List[float], embedding2: List[float]):
        self.embedding1 = embedding1
        self.embedding2 = embedding2

class EmbeddingForSearchRequest(EmbeddingRequest):
    def __init__(self, query_texts: Union[str, List[str]], document_texts: List[str], model: str = "gemini-embedding-001"):
        super().__init__(query_texts, model)
        self.document_texts = document_texts

    def to_client_query_payload(self) -> List[str]:
        if isinstance(self.texts, str):
            return [self.texts]
        return self.texts
    
    def to_client_document_payload(self) -> List[str]:
        return self.document_texts
