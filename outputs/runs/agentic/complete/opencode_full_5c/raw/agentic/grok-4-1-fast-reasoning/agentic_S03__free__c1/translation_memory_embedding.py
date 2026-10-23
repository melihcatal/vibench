import cohere
import os
from typing import List
from translation_models import Embeddings


def embed_translated_segments(segments: List[str]) -> Embeddings:
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)
    response = co.embed(texts=segments, model="embed-multilingual-v3.0")
    return response.embeddings
