
import os
import cohere
from document_client import get_cohere_client
from document_models import DocumentEmbedding

def ocr_embedding(payload, config=None):
    config = config or {}
    
    cohere_api_key = os.environ.get("COHERE_API_KEY") or config.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("Missing COHERE_API_KEY environment variable/config.")

    client = get_cohere_client(cohere_api_key)

    text_to_embed = payload['text']
    model_name = config.get("COHERE_EMBED_MODEL", "embed-english-v3.0") # Default Cohere embed model

    response = client.embed(
        texts=[text_to_embed],
        model=model_name,
        input_type="search_document" # or "clustering", "classification", "retrieval_document", "retrieval_query", "reranker"
    )

    return DocumentEmbedding(embedding_vector=response.embeddings[0])
