import boto3
from model_client import get_bedrock_client

def stream_platform_generation(payload: dict, config: dict = None):
    """
    Streams output from an AWS Bedrock managed model while preserving provider response objects.
    """
    config = config or {}
    client = get_bedrock_client(region_name=config.get("region", "us-east-1"))
    
    model_id = config.get("modelId", "us.amazon.nova-pro-v1:0")
    
    response = client.converse_stream(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )

    for chunk in response["stream"]:
        if "contentBlockDelta" in chunk and "text" in chunk["contentBlockDelta"]["delta"]:
            yield {"text": chunk["contentBlockDelta"]["delta"]["text"], "_provider_chunk": chunk}
        elif "messageStart" in chunk:
            yield {"text": "", "_provider_chunk": chunk}
        elif "messageStop" in chunk:
            yield {"text": "", "_provider_chunk": chunk}
        elif "contentBlockStop" in chunk:
            yield {"text": "", "_provider_chunk": chunk}
