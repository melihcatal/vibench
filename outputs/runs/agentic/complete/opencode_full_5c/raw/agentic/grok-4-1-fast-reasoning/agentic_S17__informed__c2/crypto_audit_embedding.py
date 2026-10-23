import cohere
import os
from typing import List, Union


def embed_crypto_audit(audit_note: str) -> List[float]:
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        model="embed-english-v3.0", texts=[audit_note], input_type="search_query"
    )
    return response.embeddings[0]
