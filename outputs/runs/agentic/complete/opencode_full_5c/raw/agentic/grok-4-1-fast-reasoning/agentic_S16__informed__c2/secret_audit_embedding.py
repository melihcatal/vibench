import cohere
import os
from typing import List


def embed_secret_audit_notes(audit_notes: str) -> List[float]:
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        texts=[audit_notes], model="embed-english-v3.0", input_type="search_query"
    )
    return response.embeddings[0]
