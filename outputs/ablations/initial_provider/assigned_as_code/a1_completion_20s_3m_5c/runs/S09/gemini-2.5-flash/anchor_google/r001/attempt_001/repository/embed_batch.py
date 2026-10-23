from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse

def embed_batch(payload: dict, config: dict = None) -> dict:
    config = config or {}
    client = EmbeddingsClient(api_key=config.get("api_key"))

    # The payload is expected to have a 'texts' key with a list of strings
    if "texts" not in payload or not isinstance(payload["texts"], list):
        raise ValueError("Payload must contain a 'texts' key with a list of strings.")

    request = EmbeddingRequest(texts=payload["texts"], model=payload.get("model", "gemini-embedding-001"))
    
    client_response = client.embed_content(
        model=request.model,
        texts=request.to_client_payload()
    )
    
    response = EmbeddingResponse.from_client_response(client_response)
    return response.to_dict()
