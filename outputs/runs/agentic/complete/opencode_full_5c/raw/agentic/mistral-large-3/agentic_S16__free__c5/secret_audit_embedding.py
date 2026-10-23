from sentence_transformers import SentenceTransformer
from security_models import SecretResponse
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def secret_audit_embedding(secret_response: SecretResponse) -> Dict[str, Any]:
    text_parts = []

    if secret_response.labels:
        text_parts.append(
            "Labels: "
            + ", ".join([f"{k}={v}" for k, v in secret_response.labels.items()])
        )

    if secret_response.notes:
        text_parts.append("Notes: " + secret_response.notes)

    text_parts.append(f"Secret ID: {secret_response.secret_id}")
    text_parts.append(f"Version: {secret_response.version_id}")

    combined_text = " | ".join(text_parts)
    embedding = model.encode(combined_text)

    return {
        "secret_id": secret_response.secret_id,
        "version_id": secret_response.version_id,
        "embedding": embedding.tolist(),
        "model": "all-MiniLM-L6-v2",
        "provider": "sentence-transformers",
    }
