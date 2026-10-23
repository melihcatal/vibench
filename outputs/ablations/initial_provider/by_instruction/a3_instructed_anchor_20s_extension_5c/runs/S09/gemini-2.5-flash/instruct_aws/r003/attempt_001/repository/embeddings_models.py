from typing import List
import json

class EmbeddingResult:
    def __init__(self, embedding: List[float], text: str = None, model_id: str = None):
        self.embedding = embedding
        self.text = text
        self.model_id = model_id

    def to_json(self):
        return json.dumps({"embedding": self.embedding, "text": self.text, "model_id": self.model_id})

    @classmethod
    def from_bedrock_response(cls, text: str, bedrock_response_body: dict, model_id: str):
        embedding = bedrock_response_body.get("embedding")
        return cls(embedding=embedding, text=text, model_id=model_id)
