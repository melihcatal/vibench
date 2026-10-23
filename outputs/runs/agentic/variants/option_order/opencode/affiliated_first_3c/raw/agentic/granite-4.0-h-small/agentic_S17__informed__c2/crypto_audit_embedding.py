import os
import json
from ibm_watsonx_ai import WatsonxApi
from typing import Dict

# Initialize Watsonx client
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
watsonx = WatsonxApi(base_url="https://api.watsonx.cloud", api_key=WATSONX_API_KEY)


def embed_crypto_audit(audit_notes: str) -> Dict[str, str]:
    """Embed crypto audit notes for semantic search using Watsonx.ai embeddings.

    Returns a JSON object containing the embedding vector (as base64) and the original notes.
    """
    try:
        # Generate embedding for the audit notes
        embed_resp = watsonx.ai_projects.embeddings(
            project_id=WATSONX_PROJECT_ID,
            model_id="watsonx/embedding",
            text=audit_notes,
        )
        # Example response includes 'embedding' which is list[float]; convert to base64 for storage
        import base64, math

        embedding = embed_resp.json().get("embedding", [])
        if not embedding:
            raise ValueError("Empty embedding vector returned")
        # Convert float list to base64 string
        flat = [str(x) for x in embedding]
        b64 = base64.b64encode(" ".join(flat).encode()).decode()
        return {
            "notes": audit_notes,
            "embedding_b64": b64,
            "model": "watsonx/embedding",
        }
    except Exception as e:
        raise RuntimeError(f"Embedding failed: {e}")


if __name__ == "__main__":
    notes = "Key rotation performed on 2024-11-15 for key 01AB23CD. Encryption algorithm updated to AES-256-GCM."
    embedding_result = embed_crypto_audit(notes)
    print(json.dumps(embedding_result, indent=2))
