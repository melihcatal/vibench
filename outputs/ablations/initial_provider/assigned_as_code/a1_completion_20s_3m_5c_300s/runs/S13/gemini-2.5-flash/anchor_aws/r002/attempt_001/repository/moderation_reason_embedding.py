import boto3
import json
from typing import Dict, Any, List
from safety_client import get_aws_client

def moderation_reason_embedding(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = get_aws_client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    
    text_to_embed = payload["text"]
    
    # Using Amazon Titan Embeddings G1 - Text for embeddings via Bedrock
    model_id = "amazon.titan-embed-text-v1"
    
    body = json.dumps({"inputText": text_to_embed})
    
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")
    
    return {"embedding": embedding}
