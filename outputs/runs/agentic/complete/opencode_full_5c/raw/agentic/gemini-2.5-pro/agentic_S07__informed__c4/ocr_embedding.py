import os
from typing import List
import cohere


def ocr_embedding(document_sections: List[str]) -> List[List[float]]:
    """
    Embed extracted document sections for semantic retrieval.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=document_sections,
        model="embed-english-v3.0",
        input_type="search_document",
    )

    return response.embeddings
