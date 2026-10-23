import os
from openai import OpenAI
from typing import List


def get_audit_note_embedding(audit_note: str) -> List[float]:
    """
    Embeds secret audit notes for semantic search using OpenAI.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.embeddings.create(
            input=audit_note, model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error creating embedding with OpenAI: {e}")
        return []


if __name__ == "__main__":
    note = "User 'admin' accessed secret 'prod/db/password' on 2024-10-26."
    embedding = get_audit_note_embedding(note)
    if embedding:
        print(f"Successfully created embedding for audit note.")
        print(f"Embedding dimensions: {len(embedding)}")
    else:
        print("Failed to create embedding.")
