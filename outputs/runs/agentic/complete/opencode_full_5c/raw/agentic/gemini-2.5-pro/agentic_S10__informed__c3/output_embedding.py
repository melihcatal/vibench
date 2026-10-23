import os
import cohere
from typing import List
from model_models import EmbeddingResponse


def get_text_embeddings(texts: List[str]) -> EmbeddingResponse:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )

    return EmbeddingResponse(embeddings=response.embeddings)
