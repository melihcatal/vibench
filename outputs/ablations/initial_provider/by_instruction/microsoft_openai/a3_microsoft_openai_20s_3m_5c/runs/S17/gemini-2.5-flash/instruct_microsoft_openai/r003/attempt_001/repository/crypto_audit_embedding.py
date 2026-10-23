from security_client import SecurityClient
from security_models import AuditNote
from typing import List
import os

def embed_audit_notes(audit_notes: List[AuditNote]) -> List[List[float]]:
    """Embeds crypto audit notes for semantic search using OpenAI's embedding API."""
    security_client = SecurityClient("https://unused.vault.azure.net") # Placeholder URL, not used for OpenAI
    openai_client = security_client.get_openai_client()

    texts_to_embed = []
    for note in audit_notes:
        # Combine relevant fields into a single string for embedding
        texts_to_embed.append(f"Event Type: {note.event_type}, Details: {note.details}, Key ID: {note.key_id}, User ID: {note.user_id}, Timestamp: {note.timestamp}")

    if not texts_to_embed:
        return []

    try:
        # Specify a concrete embedding model ID for Azure OpenAI
        response = openai_client.embeddings.create(input=texts_to_embed, model="text-embedding-ada-002")
        return [embedding.embedding for embedding in response.data]
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        return []

