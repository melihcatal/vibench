from typing import Union, List
from security_client import get_openai_client


def embed_crypto_audit_notes(notes: Union[str, bytes]) -> List[float]:
    client = get_openai_client()
    text = notes.decode("utf-8") if isinstance(notes, bytes) else str(notes)
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding
