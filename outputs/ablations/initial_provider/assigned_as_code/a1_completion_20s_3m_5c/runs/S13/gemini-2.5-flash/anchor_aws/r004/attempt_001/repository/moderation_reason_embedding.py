import boto3
import json
from typing import Dict, Any, List
from safety_client import get_aws_client
from safety_models import EmbeddingRequest, EmbeddingResult

def moderation_reason_embedding(payload: EmbeddingRequest, config: Dict[str, Any] = None) -> EmbeddingResult:
    config = config or {}
    client = get_aws_client("bedrock-runtime", config)

    # Using Amazon Titan Embeddings G1 - Text as an example model on Bedrock
    model_id = config.get("bedrock_embedding_model_id", "amazon.titan-embed-text-v1")

    body = json.dumps({
        "inputText": payload.text_to_embed
    })

    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding", [])

    return EmbeddingResult(embedding=embedding)
