import json
from storage_client import get_bedrock_runtime_client
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse


def embed_asset_metadata(
    request: AssetMetadataEmbeddingRequest,
) -> AssetMetadataEmbeddingResponse:
    bedrock_runtime = get_bedrock_runtime_client()

    # Amazon Titan Embeddings specific payload
    body = json.dumps({"inputText": request.text})

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=request.model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")

    return AssetMetadataEmbeddingResponse(embedding=embedding)
