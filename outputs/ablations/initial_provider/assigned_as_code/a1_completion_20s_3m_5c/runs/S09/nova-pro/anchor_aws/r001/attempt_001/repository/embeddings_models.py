from typing import Dict


class EmbeddingRequest:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self) -> Dict:
        return {"text": self.text}


class EmbeddingResponse:
    def __init__(self, embedding: list):
        self.embedding = embedding

    def to_dict(self) -> Dict:
        return {"embedding": self.embedding}