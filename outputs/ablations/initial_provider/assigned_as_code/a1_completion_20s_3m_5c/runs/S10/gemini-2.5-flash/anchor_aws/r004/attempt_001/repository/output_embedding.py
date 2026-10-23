from model_client import BedrockModelClient
from model_models import EmbeddingsRequest, EmbeddingsResponse

def embed_output(payload: EmbeddingsRequest, config=None) -> EmbeddingsResponse:
    client = BedrockModelClient(region_name=config.get("region") if config else None)

    # Use a specific embedding model from Bedrock
    embedding_model_id = config.get("embedding_model_id", "amazon.titan-embed-text-v1")
    response = client.get_embeddings(request=payload, model_id=embedding_model_id)
    return response
