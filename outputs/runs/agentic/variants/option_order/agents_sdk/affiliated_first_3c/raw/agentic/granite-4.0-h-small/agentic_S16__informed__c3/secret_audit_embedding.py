import os
import json
from ibm_watsonx_ai.nlp.embeddings import EmbeddingModel
from ibm_watsonx_ai import APIClient


def secret_audit_embedding(secret_id: str, secret_version: str = "latest") -> dict:
    """Embed secret audit notes for downstream semantic search using watsonx.ai embeddings."""
    from security_client import SecretsClient
    client = SecretsClient()
    payload = client.get_secret(secret_id, secret_version)
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError("Missing WATSONX_API_KEY or WATSONX_PROJECT_ID")
    client = APIClient(authenticator=APIClient.ApiKeyAuthenticator(api_key))
    model = EmbeddingModel(model_id="ibm/granite-embed-001")  # example embedding model
    response = model.encode_text(json.dumps(payload))
    embedding = response.get_result()
    return {
        "secret_id": secret_id,
        "version": secret_version,
        "embedding": embedding
    }
