import os
import cohere
from document_models import EmbeddingResponse


def ocr_embedding(text: str) -> EmbeddingResponse:
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)
    response = co.embed(texts=[text], model="embed-english-v3.0")
    return {"embedding": response.embeddings[0]}
