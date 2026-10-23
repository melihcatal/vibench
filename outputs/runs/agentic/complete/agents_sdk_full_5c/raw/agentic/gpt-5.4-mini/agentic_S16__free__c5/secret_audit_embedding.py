import os
from typing import List

from security_client import get_secret_manager_client

# OpenAI embeddings provider signal
from openai import OpenAI


def secret_audit_embedding(notes: List[str], model: str = "text-embedding-3-small"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = "\n".join(notes)
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
