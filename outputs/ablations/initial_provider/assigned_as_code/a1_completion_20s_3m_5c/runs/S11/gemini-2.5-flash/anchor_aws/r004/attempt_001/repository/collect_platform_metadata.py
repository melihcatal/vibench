import boto3

def collect_platform_metadata(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    model_id = config.get("model_id", "us.amazon.nova-pro-v1:0")
    
    response = client.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )
    
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    
    metadata = {
        "invocation_metrics": response.get("amazon-bedrock-invocation-metrics"),
        "usage": response.get("usage"), # Contains input/output token counts
        "model_id": model_id,
        "response_id": response["output"]["responseId"]
    }
    
    return {"text": text, "metadata": metadata}
