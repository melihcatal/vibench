from safety_client import DEFAULT_EMBEDDING_MODEL, get_client, get_model
from safety_models import normalize_text


def moderation_reason_embedding(text, model=None):
    client = get_client()
    embedding_model = get_model(model, DEFAULT_EMBEDDING_MODEL)
    response = client.embeddings.create(model=embedding_model, input=normalize_text(text))
    return {"embedding": response.data[0].embedding, "raw": response.model_dump()}
