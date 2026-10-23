from document_client import get_cohere_client
from typing import List

def ocr_embedding(sections: List[str]) -> List[List[float]]:
    if not sections:
        return []
    client = get_cohere_client()
    response = client.embed(
        texts=sections,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return [embedding for embedding in response.embeddings]