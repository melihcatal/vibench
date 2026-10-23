import os
from typing import List, Optional
import openai
from security_models import SecretAuditNote

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Generates an embedding for the given text using OpenAI's embedding model.
    """
    # Ensure OPENAI_API_KEY environment variable is set
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    try:
        response = openai.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise

def embed_audit_note(note: SecretAuditNote) -> SecretAuditNote:
    """
    Embeds the content of a SecretAuditNote for semantic search.
    """
    if note.note_content:
        note.embedding = get_embedding(note.note_content)
    return note

def embed_audit_notes_batch(notes: List[SecretAuditNote]) -> List[SecretAuditNote]:
    """
    Embeds a batch of SecretAuditNote contents.
    """
    for note in notes:
        if note.note_content:
            note.embedding = get_embedding(note.note_content)
    return notes
