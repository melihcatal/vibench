import os
import cohere
from typing import List
from security_models import AuditRecord

def embed_audit_notes(audit_records: List[AuditRecord]) -> List[AuditRecord]:
    """
    Generates embeddings for the 'notes' field of audit records using Cohere.

    Args:
        audit_records: A list of AuditRecord objects.

    Returns:
        The same list of AuditRecord objects with the 'embedding' field populated.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    texts_to_embed = [record.notes for record in audit_records if record.notes]

    if not texts_to_embed:
        return audit_records

    try:
        response = co.embed(
            texts=texts_to_embed,
            model='embed-english-light-v2.0',
            input_type='search_document'
        )
        
        embeddings = response.embeddings
        
        # Match embeddings back to the original records
        embedding_iter = iter(embeddings)
        for record in audit_records:
            if record.notes:
                record.embedding = next(embedding_iter)
        
        return audit_records

    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        # Return the original list without embeddings on error
        return audit_records
