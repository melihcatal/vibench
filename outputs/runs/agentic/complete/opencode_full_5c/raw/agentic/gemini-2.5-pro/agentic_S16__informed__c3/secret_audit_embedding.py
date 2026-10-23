import os
import cohere
from typing import List


def embed_audit_notes(audit_notes: List[str]) -> List[List[float]]:
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))

    response = co.embed(
        texts=audit_notes, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
