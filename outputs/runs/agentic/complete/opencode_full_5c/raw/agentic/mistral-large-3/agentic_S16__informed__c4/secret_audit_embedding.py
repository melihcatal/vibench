from openai import OpenAI
import os
import numpy as np


def secret_audit_embedding(audit_notes: str) -> list:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input=audit_notes, model="text-embedding-3-small"
    )

    return response.data[0].embedding
