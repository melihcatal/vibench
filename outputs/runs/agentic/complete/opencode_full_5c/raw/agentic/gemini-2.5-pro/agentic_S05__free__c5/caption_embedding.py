import os
import cohere
from typing import List

co = cohere.Client(os.getenv("COHERE_API_KEY"))


def embed_caption_chunk(text: str) -> List[float]:
    response = co.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings[0]
