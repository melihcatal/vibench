import os
import json
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_watsonx_ai import WatsonXAI
from security_models import SecretPayload

def embed_secret_audit(secret_name: str) -> None:
    """Extract audit notes from a secret, embed them for semantic search.
    Retrieves a secret that holds audit notes, loads it as JSON, and sends
    the text to watsonx.ai for embedding.
    The embedding ID is printed to stdout for downstream retrieval.
    """
    client = SecretsManagerV1.new_instance(
        apikey=os.getenv("SECRETS_MANAGER_APIKEY"),
        service_url=os.getenv("SECRETS_MANAGER_SERVICE_URL")
    )
    resp = client.get_secret(
        secret_type="arbitrary",
        id_or_name=secret_name,
        version_id="latest"
    ).get_result()
    payload = SecretPayload(resp["plaintext"])
    if not payload.json:
        raise ValueError("Audit notes must be valid JSON")
    audit_data = payload.json
    # Expecting audit_data to contain a field "notes"
    notes = audit_data.get("notes", "")
    # Initialize watsonx.ai client (uses WATSONX_API_KEY, WATSONX_PROJECT_ID env vars)
    wx = WatsonXAI()
    embedding = wx.embed_text(text=notes)
    print(f"Embedding stored; ID: {embedding['id']}")

if __name__ == "__main__":
    # Example audit secret containing JSON with 'notes'
    embed_secret_audit("my-audit-secret")