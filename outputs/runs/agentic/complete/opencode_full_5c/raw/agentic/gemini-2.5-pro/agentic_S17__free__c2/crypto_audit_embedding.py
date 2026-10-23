from security_client import get_cohere_client
from security_models import EmbeddingPayload


def embed_audit_notes(payload: EmbeddingPayload) -> list:
    cohere_client = get_cohere_client()

    try:
        response = cohere_client.embed(
            texts=payload.texts, model=payload.model, input_type="search_document"
        )
        return response.embeddings
    except Exception:
        return []
