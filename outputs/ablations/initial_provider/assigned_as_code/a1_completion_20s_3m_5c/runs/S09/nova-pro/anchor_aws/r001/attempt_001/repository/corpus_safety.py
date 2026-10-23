from embeddings_client import get_bedrock_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def corpus_safety(text, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    response = client.check_corpus_safety(text=text)
    return response["is_safe"]