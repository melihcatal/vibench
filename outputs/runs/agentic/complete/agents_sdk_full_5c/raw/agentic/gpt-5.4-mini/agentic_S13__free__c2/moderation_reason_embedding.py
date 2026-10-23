from openai import OpenAI

from safety_client import get_client, load_config
from safety_models import normalize_text


def moderation_reason_embedding(reason: str):
    cfg = load_config()
    client: OpenAI = get_client(cfg)
    response = client.embeddings.create(model=cfg.embedding_model, input=normalize_text(reason))
    return response.data[0].embedding if response.data else []
