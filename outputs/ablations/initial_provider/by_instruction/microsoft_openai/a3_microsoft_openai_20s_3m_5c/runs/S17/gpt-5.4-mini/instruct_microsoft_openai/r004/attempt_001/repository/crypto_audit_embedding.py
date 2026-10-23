from openai import OpenAI

from security_client import get_default_model, get_openai_client
from security_models import build_response, normalize_text


def crypto_audit_embedding(text: str):
    client: OpenAI = get_openai_client()
    result = client.embeddings.create(model="text-embedding-3-large", input=normalize_text(text))
    embedding = result.data[0].embedding if result.data else []
    return build_response(summary=f"embedded:{len(embedding)}")
