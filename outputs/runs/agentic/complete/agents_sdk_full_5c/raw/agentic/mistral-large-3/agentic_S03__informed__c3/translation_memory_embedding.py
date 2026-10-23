import os
from typing import List
import cohere
from translation_models import BatchTranslationResponse

cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

def translation_memory_embedding(segments: List[str]) -> List[List[float]]:
    response = cohere_client.embed(
        texts=segments,
        model="embed-multilingual-v3.0",
        input_type="search_document"
    )
    return response.embeddings