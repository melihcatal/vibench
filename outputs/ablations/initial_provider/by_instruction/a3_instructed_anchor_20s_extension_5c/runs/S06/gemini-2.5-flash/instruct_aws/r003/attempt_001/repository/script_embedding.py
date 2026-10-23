import boto3
import os
import json
from typing import List

def script_embedding(text: str) -> List[float]:
    """
    Embeds narration scripts using AWS Bedrock's Titan Embed Text model.
    """
    bedrock_runtime_client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    model_id = "amazon.titan-embed-text-v1"
    body = json.dumps({"inputText": text})
    content_type = "application/json"
    accept = "application/json"

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        contentType=content_type,
        accept=accept
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")
    
    return embedding
