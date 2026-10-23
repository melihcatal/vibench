from embeddings_client import get_bedrock_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def multilingual_query_translate(query, target_language, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    response = client.translate_query(query=query, target_language=target_language)
    return response["translated_query"]