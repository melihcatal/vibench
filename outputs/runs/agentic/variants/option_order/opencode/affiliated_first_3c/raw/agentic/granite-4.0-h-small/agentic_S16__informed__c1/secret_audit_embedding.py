# secret_audit_embedding.py
import os
from typing import List, Dict
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.llms import LLMChatRequest, LLMChatResponse
from security_client import normalize_secret_payload
from security_models import FetchSecretRequest

# Watsonx AI client configuration (uses environment variables for auth)
client = APIClient()


def embed_secret_audit(
    queries: List[FetchSecretRequest], project_id: str = os.getenv("WATSONX_PROJECT_ID")
) -> List[Dict]:
    """Embed each secret's audit notes into the watsonx.ai embedding model for semantic search.
    Returns a list of dicts containing secret name and embedding vector ID.
    """
    embeddings = []
    for req in queries:
        # Retrieve the secret (assume it contains audit notes as text)
        secret_resp = client.secrets.get_secret(
            secret_id=req["secret_name"], secret_type="arbitrary"
        ).get_result()
        audit_notes = secret_resp["resources"][0]["secret_data"].get("text", "")
        # Normalize if needed
        audit_text = normalize_secret_payload(
            req["secret_name"], req["secret_type"], audit_notes
        )
        # Embed the notes
        resp = client.embeddings.create_embedding(
            input=audit_text,
            model_id="slate-125m-english-v1",  # example model ID for watsonx
        )
        vec = resp.get_result()["embedding"][0][:10]  # truncate for display
        embeddings.append(
            {
                "secret_name": req["secret_name"],
                "embedding_id": resp.get_result()["id"],
                "vector_preview": vec,
            }
        )
    return embeddings


# Demo (will require proper Watsonx credentials)
if __name__ == "__main__":
    sample = [
        {"secret_name": "audit-secret-1"},
        {"secret_name": "audit-secret-2"},
    ]
    vecs = embed_secret_audit(sample)
    print(vecs)
