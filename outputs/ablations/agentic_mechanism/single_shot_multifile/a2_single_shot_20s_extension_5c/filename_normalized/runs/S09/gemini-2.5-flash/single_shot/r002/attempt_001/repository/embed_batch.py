import os
from typing import List

import cohere

def embed_batch(texts: List[str]) -> List[List[float]]:
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return response.embeddings