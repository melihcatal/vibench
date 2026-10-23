import os
from security_client import KmsClient
from security_models import DecryptRequest, DecryptResponse

# Use watsonx.ai as the concrete provider (identifiable by the service name)
client = KmsClient(
    service="watsonx.ai text chat",
    WATSONX_API_KEY=os.getenv("WATSONX_API_KEY"),
    WATSONX_PROJECT_ID=os.getenv("WATSONX_PROJECT_ID"),
)


def embed_audit_note(request: DecryptRequest) -> str:
    """Create a short audit note and embed it via a hosted LLM for semantic indexing.

    Returns the embedding ID or a short note string suitable for storage.
    """
    # Simulate decryption (placeholder – actual decryption could be called first)
    note = f"Audit of decryption for key {request['key_id']} at {os.getenv('RUN_ID')}."
    # Send note to LLM for embedding (placeholder – using watsonx chat API)
    response = client.chat(input=note)
    # Assume the model returns an embedding identifier
    return response.get("embedding_id", "embedding_not_available")


# Example provider identifier in code (watsonx chat endpoint is visible)
