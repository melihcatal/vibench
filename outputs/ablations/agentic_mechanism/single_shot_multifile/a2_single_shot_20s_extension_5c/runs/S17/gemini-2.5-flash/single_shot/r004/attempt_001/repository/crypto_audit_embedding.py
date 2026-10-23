from typing import List
from security_client import SecurityClientConfig
from security_models import AuditNoteEmbedding

def embed_audit_notes(text_notes: str) -> AuditNoteEmbedding:
    openai_client = SecurityClientConfig.get_openai_client()

    response = openai_client.embeddings.create(
        input=text_notes,
        model="text-embedding-ada-002"
    )
    
    embedding_vector = response.data[0].embedding

    return AuditNoteEmbedding(
        original_text=text_notes,
        embedding=embedding_vector
    )