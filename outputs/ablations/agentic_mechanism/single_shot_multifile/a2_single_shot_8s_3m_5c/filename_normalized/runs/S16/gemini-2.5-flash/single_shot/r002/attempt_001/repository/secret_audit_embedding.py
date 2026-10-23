import os
from typing import List
import openai
from security_models import AuditNote

def embed_audit_notes(notes: List[AuditNote], model: str = "text-embedding-3-small") -> List[AuditNote]:
    """Embeds secret audit notes using OpenAI's embedding API for semantic search.

    Each AuditNote in the input list should have its 'details' field populated.
    The 'embedding' field of each AuditNote will be updated with the generated vector.
    """
    client = openai.OpenAI()
    texts_to_embed = [note.details for note in notes if note.details is not None]

    if not texts_to_embed:
        return notes

    try:
        response = client.embeddings.create(
            input=texts_to_embed,
            model=model
        )

        for i, embedding_data in enumerate(response.data):
            if i < len(notes):
                notes[i].embedding = embedding_data.embedding

        return notes

    except openai.APIError as e:
        raise ValueError(f"OpenAI API error during embedding creation: {e}") from e
    except Exception as e:
        raise ValueError(f"An unexpected error occurred during embedding: {e}") from e
