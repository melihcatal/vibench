# secret_audit_embedding.py
# Embeds audit notes of secret usage into a vector store for semantic search.
import os
import json
from security_models import normalize_secret_payload
from dashscope import Client

# Initialize the DashScope client using the environment key
client = Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

# Define the model to use for embeddings (Qwen from DashScope)
model_id = "qwen2-72b"


def embed_audit_note(secret: dict, note: str) -> None:
    """Create a vector embedding for an audit note tied to a secret and store it.

    Args:
        secret (dict): The secret payload (any provider format).
        note (str): Human‑readable audit summary (e.g., "Accessed by user123 on 2025-08-01").

    The function stores a JSON document containing the secret identifier, normalized data, and embedding vector.
    """
    normalized = normalize_secret_payload(secret)
    # Prepare payload for DashScope embedding endpoint
    request_body = {"model": model_id, "texts": [note]}
    response = client.embeddings.create(request_body)
    embedding = response["data"][0]["embedding"]  # list of floats
    # Assemble a document to be persisted (here we just print; in real use write to a DB)
    doc = {
        "secret_id": normalized.get("username") or normalized.get("username_id"),
        "normalized": normalized,
        "audit_note": note,
        "embedding": embedding,
    }
    # Example persistence (using a placeholder JSON file)
    with open("audit_embeddings.json", "a") as f:
        json.dump(doc, f)
        f.write("\n")


if __name__ == "__main__":
    # Demo: embed a sample audit note for a dummy secret
    demo_secret = {"username": "alice", "password": "s3cr3t"}
    audit_note = "User accessed the secret for configuration update on 2025-08-01."
    embed_audit_note(demo_secret, audit_note)
    print("Audit embedding created (see audit_embeddings.json)")
