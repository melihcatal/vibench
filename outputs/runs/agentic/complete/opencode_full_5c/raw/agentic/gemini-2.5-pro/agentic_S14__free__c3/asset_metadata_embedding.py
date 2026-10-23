import json
from typing import List
from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingRequest


def create_metadata_embedding(request: EmbeddingRequest) -> List[float]:
    """
    Creates a text embedding using Amazon Titan Embeddings G1 - Text on Bedrock.
    """
    bedrock_client = get_bedrock_runtime_client()

    body = json.dumps({"inputText": request.text_to_embed})

    model_id = "amazon.titan-embed-text-v1"
    accept = "application/json"
    content_type = "application/json"

    response = bedrock_client.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )

    response_body = json.loads(response.get("body").read())
    return response_body.get("embedding", [])
