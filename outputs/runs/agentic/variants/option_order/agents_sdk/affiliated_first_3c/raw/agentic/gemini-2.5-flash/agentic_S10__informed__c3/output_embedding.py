from model_client import GeminiClient
from typing import List

class EmbeddingResult:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding

def get_embedding(text: str, model_id: str = "models/embedding-001") -> EmbeddingResult:
    client = GeminiClient()
    model = client.get_embedding_model(model_id)

    response = model.embed_content(content=text, task_type="RETRIEVAL_DOCUMENT") # Or other task types like CLASSIFICATION, QA_PAIR, etc.

    if response.embedding and response.embedding.values:
        return EmbeddingResult(embedding=list(response.embedding.values))
    else:
        raise ValueError("Failed to retrieve embedding.")
