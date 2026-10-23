from embeddings_client import get_bedrock_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def retrieval_audio_brief(search_results, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    response = client.generate_audio_brief(search_results=search_results)
    return response["audio_brief"]