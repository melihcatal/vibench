import cohere
import os
from typing import List


def embed_secret_audit_notes(notes_list: List[str]) -> List[list[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=notes_list, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
