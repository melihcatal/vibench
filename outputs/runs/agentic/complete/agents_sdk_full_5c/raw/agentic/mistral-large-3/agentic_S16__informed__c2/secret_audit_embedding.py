import cohere
import os

from security_models import EmbeddingResponse

def secret_audit_embedding(text: str) -> EmbeddingResponse:
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return EmbeddingResponse(
        embedding=response.embeddings[0],
        model="embed-english-v3.0"
    )