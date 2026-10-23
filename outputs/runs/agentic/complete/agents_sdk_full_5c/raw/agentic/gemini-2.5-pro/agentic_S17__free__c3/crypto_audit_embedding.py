from typing import List
from security_client import cohere_client
from security_models import AuditNote, EmbeddingResponse

def embed_audit_notes(notes: List[AuditNote]) -> EmbeddingResponse:
    """
    Embeds crypto audit notes for semantic search using Cohere.
    """
    try:
        client = cohere_client.get_client()
        
        texts_to_embed = [
            f"Event: {note.event_name}, User: {note.user}, Details: {note.details}"
            for note in notes
        ]
        
        response = client.embed(
            texts=texts_to_embed,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        
        return EmbeddingResponse(
            vectors=response.embeddings,
            success=True
        )
    except Exception as e:
        return EmbeddingResponse(
            vectors=[],
            success=False,
            error=str(e)
        )
