import cohere
from security_client import get_cohere_api_key
from security_models import AuditEmbedding

def embed_audit_note(note_id: str, note_text: str) -> AuditEmbedding | None:
    """
    Embeds secret audit notes for semantic search using the Cohere API.

    Args:
        note_id: A unique identifier for the audit note.
        note_text: The text content of the audit note.

    Returns:
        An AuditEmbedding object containing the original text and its embedding,
        or None if an error occurs.
    """
    api_key = get_cohere_api_key()
    if not api_key:
        print("Cohere API key not found. Please set the COHERE_API_KEY environment variable.")
        return None

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[note_text],
            model='embed-english-v3.0',
            input_type='search_document'
        )
        
        embedding = response.embeddings[0]
        
        return AuditEmbedding(
            note_id=note_id,
            text=note_text,
            embedding=embedding
        )

    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return None

# Example usage would be in a different file.
# if __name__ == "__main__":
#     audit_note = "User 'admin' accessed the production database credentials on 2023-10-27."
#     note_identifier = "audit-log-12345"

#     embedding_result = embed_audit_note(note_identifier, audit_note)

#     if embedding_result:
#         print(f"Successfully created embedding for note ID: {embedding_result.note_id}")
#         print(f"Original text: '{embedding_result.text}'")
#         # The embedding itself is very long, so we just show its dimensions
#         print(f"Embedding dimensions: {len(embedding_result.embedding)}")
#     else:
#         print("Failed to create embedding for the audit note.")
