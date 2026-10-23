from model_client import LLMClientFactory
from model_models import EmbeddingRequest, EmbeddingResponse
import os

def embed_model_outputs(request: EmbeddingRequest) -> EmbeddingResponse:
    client = LLMClientFactory.get_cohere_client()

    embedding_model = "embed-english-v3.0"
    
    embed_type = "search_document"

    response = client.embed(
        texts=request.texts,
        model=embedding_model,
        input_type=embed_type,
    )

    embeddings = response.embeddings
    return EmbeddingResponse(embeddings=embeddings)