import boto3
import json
from model_client import get_bedrock_client

def invoke_bedrock_model(
    prompt: str,
    model_id: str,
    temperature: float = 0.7,
    max_tokens: int = 512,
) -> dict:
    """
    Invokes a provider-managed model (AWS Bedrock) through a platform client.
    """
    client = get_bedrock_client()

    body = json.dumps({
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens_to_sample": max_tokens
    })

    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    return response_body
