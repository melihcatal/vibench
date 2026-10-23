import json
from typing import List
from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingRequest


def get_asset_metadata_embedding(request: EmbeddingRequest) -> List[float]:
    """
    Generates an embedding for asset metadata and text using Amazon Titan Embeddings.
    """
    bedrock_client = get_bedrock_runtime_client()

    combined_text = f"Metadata: {json.dumps(request.metadata)}\nContent: {request.text}"

    body = json.dumps(
        {
            "inputText": combined_text,
        }
    )

    model_id = "amazon.titan-embed-text-v1"
    response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())

    return response_body.get("embedding")
