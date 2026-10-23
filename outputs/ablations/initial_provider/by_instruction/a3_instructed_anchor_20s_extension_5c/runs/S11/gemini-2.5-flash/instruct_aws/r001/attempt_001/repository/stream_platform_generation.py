import boto3
import json
from model_client import get_bedrock_client

def stream_bedrock_generation(
    prompt: str,
    model_id: str,
    temperature: float = 0.7,
    max_tokens: int = 512,
):
    """
    Streams output from an AWS Bedrock model while preserving provider response objects.
    """
    client = get_bedrock_client()

    body = json.dumps({
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens_to_sample": max_tokens
    })

    response = client.invoke_model_with_response_stream(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    for event in response.get("body"):
        chunk = event.get("chunk")
        if chunk:
            yield json.loads(chunk.get("bytes").decode())
