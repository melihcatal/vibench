import boto3

def collect_platform_metadata(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse(
        modelId="us.amazon.nova-pro-v1:0", # Using the same model as invoke_platform_model.py
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    
    metadata = {
        "usage": response.get("usage"),
        "amazon_bedrock_model_id": response["output"]["message"]["modelId"], # Example of extracting a model ID
        # Add other relevant metadata here based on the Bedrock response structure
    }
    
    return {"text": text, "metadata": metadata}
