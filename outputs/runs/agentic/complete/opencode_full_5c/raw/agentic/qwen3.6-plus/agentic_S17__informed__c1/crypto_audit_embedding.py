import os
from openai import OpenAI
from typing import List, Dict, Optional


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))


def embed_audit_notes(
    audit_notes: List[str],
    model: str = "text-embedding-3-small",
) -> Dict:
    if not audit_notes:
        return {
            "embeddings": [],
            "model": model,
            "usage": {"prompt_tokens": 0, "total_tokens": 0},
            "request_id": "",
        }

    response = client.embeddings.create(
        input=audit_notes,
        model=model,
    )

    embeddings = [item.embedding for item in response.data]

    return {
        "embeddings": embeddings,
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        "request_id": response.id if hasattr(response, "id") else "",
    }


def embed_single_note(
    note: str,
    model: str = "text-embedding-3-small",
) -> Dict:
    return embed_audit_notes([note], model=model)


if __name__ == "__main__":
    sample_notes = [
        "Key rotation completed successfully for key arn:aws:kms:us-east-1:123456789012:key/abc123 on 2024-01-15.",
        "Encryption policy updated to require AES-256-GCM for all new data keys.",
        "Access audit: User admin@example.com performed 15 Decrypt operations in the last 24 hours.",
    ]
    result = embed_audit_notes(sample_notes)
    print(result)
