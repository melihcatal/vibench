import boto3
from model_client import get_bedrock_client

def collect_platform_metadata(payload: dict, config: dict = None):
    """
    Returns model output together with AWS Bedrock platform metadata.
    """
    config = config or {}
    client = get_bedrock_client(region_name=config.get("region", "us-east-1"))
    
    model_id = config.get("modelId", "us.amazon.nova-pro-v1:0")

    response = client.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )

    text_content = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    
    metadata = {
        "modelId": response["output"]["responseMetadata"]["modelId"],
        "usage": response["usage"],
        "stopReason": response["output"]["stopReason"],
        "_provider_response": response # Keep the full provider response for comprehensive metadata
    }

    return {"text": text_content, "metadata": metadata}
