import cohere
import os
from typing import List

def ocr_embedding(sections: List[str]) -> List[List[float]]:
    """Embed extracted document sections for semantic retrieval."""
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        texts=sections,
        model="embed-english-v3.0"
    )
    return response.embeddings
