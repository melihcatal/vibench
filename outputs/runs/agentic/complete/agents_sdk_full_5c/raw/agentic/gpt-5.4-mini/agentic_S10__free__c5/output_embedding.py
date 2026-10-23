from openai import OpenAI

from model_client import get_client, select_embedding_model
from model_models import NormalizedEmbeddingResponse, normalize_embedding_response


PROVIDER = "openai"
DEFAULT_MODEL = "text-embedding-3-small"


def output_embedding(text: str) -> NormalizedEmbeddingResponse:
    client = get_client()
    model = select_embedding_model(default=DEFAULT_MODEL)
    resp = client.embeddings.create(model=model, input=text)
    return normalize_embedding_response(resp)
