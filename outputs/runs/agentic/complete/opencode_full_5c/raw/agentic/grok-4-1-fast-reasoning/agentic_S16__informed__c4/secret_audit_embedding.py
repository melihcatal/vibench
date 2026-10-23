import cohere
import os
from typing import List


def embed_secret_audit_notes(audit_notes: List[str]) -> List[List[float]]:
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(
        model="embed-english-v3.0", texts=audit_notes, input_type="search_query"
    )
    return response.embeddings
