import os
from typing import List, Dict, Any
from translation_client import get_cohere_client
from translation_models import create_embedding_result

def embed_segments(texts: List[str]) -> List[Dict[str, Any]]:
    client = get_cohere_client()

    response = client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )

    embeddings = response.embeddings
    results = []
    for i, text in enumerate(texts):
        results.append(create_embedding_result(text=text, embedding=embeddings[i]))
    return results
