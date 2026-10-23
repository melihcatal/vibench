import os
import cohere
from embeddings_models import EmbeddingResponse

def embed_batch(texts: list[str]) -> list[EmbeddingResponse]:
    """Generates embeddings for a batch of texts using Cohere."""
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))
    model_name = "embed-english-v3.0"
    response = co.embed(
        texts=texts,
        model=model_name,
        input_type="search_document"
    )
    embeddings = response.embeddings
    
    results = []
    for i, text in enumerate(texts):
        results.append(EmbeddingResponse(text=text, embedding=embeddings[i], model=model_name))
    return results