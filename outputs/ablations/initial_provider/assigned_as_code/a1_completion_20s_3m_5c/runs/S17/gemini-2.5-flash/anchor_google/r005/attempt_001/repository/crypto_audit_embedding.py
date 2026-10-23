from security_models import CryptoAuditEmbeddingConfig
from security_client import get_cohere_client

def embed_audit_notes(audit_notes: list[str], config: CryptoAuditEmbeddingConfig):
    client = get_cohere_client(config.cohere_api_key)

    response = client.embed(
        texts=audit_notes,
        model=config.model,
        input_type="search_document"
    )

    return {"embeddings": response.embeddings}
