import os
from security_client import get_openai_client
from security_models import AuditNoteEmbedding


def embed_audit_note(note_id: str, audit_note: str) -> AuditNoteEmbedding:
    client = get_openai_client()
    try:
        response = client.embeddings.create(
            input=audit_note, model="text-embedding-3-small"
        )
        embedding = response.data[0].embedding
        return AuditNoteEmbedding(note_id=note_id, embedding=embedding)
    except Exception as e:
        # In a real scenario, you might want to log the error or handle it more gracefully
        print(f"Error creating embedding for note_id {note_id}: {e}")
        return AuditNoteEmbedding(
            note_id=note_id, embedding=[]
        )  # Return empty embedding on error
