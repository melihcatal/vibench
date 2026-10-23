from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingRequest, EmbeddingResponse
import json


def embed_asset_metadata(request: EmbeddingRequest) -> EmbeddingResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()

    # For Amazon Titan Embeddings
    if request.model_id == "amazon.titan-embed-text-v1":
        body = json.dumps({"inputText": request.text})
        model_id = request.model_id
    else:
        raise ValueError(f"Unsupported model ID for embedding: {request.model_id}")

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")

    return EmbeddingResponse(embedding=embedding, raw_response=response_body)
