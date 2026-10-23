import openai
from typing import List
from security_client import get_openai_key
from security_models import AuditEmbedding


def embed_secret_audit_notes(notes: List[str]) -> List[AuditEmbedding]:
    key = get_openai_key()
    client = openai.OpenAI(api_key=key)
    response = client.embeddings.create(input=notes, model="text-embedding-3-small")
    return [
        {"embedding": embedding.embedding, "note": notes[i]}
        for i, embedding in enumerate(response.data)
    ]
