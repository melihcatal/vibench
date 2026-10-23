from security_client import get_model_name, get_openai_client
from security_models import normalize_text


def crypto_audit_embedding(note):
    client = get_openai_client()
    embedding = client.embeddings.create(model=get_model_name(), input=normalize_text(note))
    vector = embedding.data[0].embedding if embedding.data else []
    return {"embedding": vector, "provider": "openai"}
