import openai
import os
from typing import List


def generate_crypto_audit_embedding(audit_notes: str) -> List[float]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=audit_notes, model="text-embedding-3-small"
    )
    return [float(x) for x in response.data[0].embedding]
