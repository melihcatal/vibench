# [LATER-STEP] crypto_audit_embedding.py
# Embed crypto audit notes for semantic search using IBM watsonx.ai embeddings

import os
from ibm_watsonx_ai.service_util.embeddings import EmbeddingsClient
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class AuditEmbedder:
    """Embeds audit notes so they can be queried via semantic search."""

    def __init__(self):
        api_key = os.getenv("WATSONX_API_KEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        if not api_key or not project_id:
            raise RuntimeError("Set WATSONX_API_KEY and WATSONX_PROJECT_ID env vars")
        authenticator = IAMAuthenticator(api_key)
        self._client = EmbeddingsClient(
            authenticator=authenticator, project_id=project_id
        )

    def embed_note(self, note: str) -> str:
        """Returns a base64‑encoded embedding vector for a given audit note."""
        response = self._client.create_embeddings(
            input_text=note,
            # Use the Granite model family – here we request the 7B instruct model
            provider_model="granite-7b-instruct",
        ).get_result()
        # The response contains a JSON array of floats; we encode as base64
        import base64

        vectors = response["embeddings"][0]["vector"]
        return base64.b64encode(json.dumps(vectors).encode()).decode()


# Example usage (for testing)
if __name__ == "__main__":
    embedder = AuditEmbedder()
    vec = embedder.embed_note(
        "User decrypted a sensitive payroll record using key key-83."
    )
    print("Embedding vector (base64):", vec)
