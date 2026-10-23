from openai import OpenAI
from typing import List
from security_client import get_secrets_config

def embed_secret_audit_notes(audit_notes: str) -> List[float]:
    config = get_secrets_config()
    api_key = config['openai_api_key']
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=audit_notes
    )
    return [float(d) for d in response.data[0].embedding]