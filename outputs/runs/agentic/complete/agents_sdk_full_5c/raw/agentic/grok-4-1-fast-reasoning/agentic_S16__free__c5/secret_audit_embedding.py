from openai import OpenAI
from typing import List, Any
from security_client import get_openai_config

def embed_secret_audit_notes(notes: List[str]) -> List[List[float]]:
    config = get_openai_config()
    client = OpenAI(api_key=config['api_key'])
    response = client.embeddings.create(
        input=notes,
        model="text-embedding-3-small"
    )
    return [item.embedding for item in response.data]
