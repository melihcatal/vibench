import boto3

def collect_platform_metadata(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse(
        modelId="us.amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)

    # Extract relevant metadata from the response
    metadata = {
        "usage": response.get("usage"),
        "stop_reason": response.get("stopReason"),
        "model_id": response.get("modelId"),
        # Add other relevant metadata fields as needed
    }

    return {"text": text, "metadata": metadata, "_original_response": response}
