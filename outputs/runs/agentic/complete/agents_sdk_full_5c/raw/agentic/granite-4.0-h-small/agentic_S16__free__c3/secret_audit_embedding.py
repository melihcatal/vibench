# secret_audit_embedding.py
import openai
from security_models import SecretReadResponse
from security_client import get_secret_manager_client

def embed_audit(secret_name: str, model: str = 'text-embedding-ada-002') -> str:
    """Embed audit notes for a secret into a vector for semantic search.

    Uses OpenAI's embedding model as the concrete provider.
    Returns the embedding ID (in practice you would store the vector). 
    """
    client = get_secret_manager_client()
    version = client.access_secret_version(name=secret_name)
    payload = version.payload.data.decode('UTF-8')
    audit_notes = json.loads(payload).get('audit_notes', '')
    if not audit_notes:
        return "No audit notes found."
    response = openai.Embedding.create(
        model=model,
        input=audit_notes,
    )
    embedding_id = response['data'][0]['embedding_id']
    return embedding_id
```