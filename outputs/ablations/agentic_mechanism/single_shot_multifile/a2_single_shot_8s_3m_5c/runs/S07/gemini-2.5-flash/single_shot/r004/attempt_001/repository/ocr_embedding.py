import os
import cohere
from document_client import get_cohere_client
from document_models import EmbeddingResult

def embed_document_section(text: str, model_name: str = "embed-english-v3.0", input_type: str = "search_document") -> EmbeddingResult:
    client = get_cohere_client()

    response = client.embed(
        texts=[text],
        model=model_name,
        input_type=input_type
    )

    embedding = response.embeddings[0]

    return EmbeddingResult(embedding=embedding, text=text)