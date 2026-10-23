import json
import os
from typing import List
from datetime import datetime
from openai import OpenAI
from security_models import SecretEntry, SecretAuditResult

# Load OpenAI API key from environment (managed secret)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Embedding model to use (Azure OpenAI example)
EMBEDDING_MODEL = "text-embedding-ada-002"


# Helper to generate an embedding for audit notes
def create_embedding(text: str) -> List[float]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding  # List of floats


# Store embedding vectors with secret metadata
def secret_audit_embedding(entries: List[SecretEntry]) -> List[dict]:
    now = datetime.utcnow().isoformat() + "Z"
    results = []
    for entry in entries:
        note = entry.get("description", "")
        embedding = create_embedding(note)
        results.append(
            {
                "entry": entry,
                "embedding": embedding.tolist(),
                "fetched_at": now,
            }
        )
    return results


# Example usage (remove in production code)
if __name__ == "__main__":
    sample_entries = [
        {
            "name": "db-prod",
            "label": "production",
            "description": "production database credentials",
        },
        {"name": "api-key", "label": "api", "description": "api secret key"},
    ]
    print(json.dumps(secret_audit_embedding(sample_entries), indent=2))
