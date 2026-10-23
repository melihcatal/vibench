import boto3

def collect_platform_metadata(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
        inferenceConfig={
            "maxTokens": config.get("max_tokens", 512),
            "temperature": config.get("temperature", 0.5),
        },
    )

    text_output = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    
    metadata = {
        "usage": response.get("usage"),
        "amazon_model_id": response["output"]["responseMetadata"]["modelId"],
        "request_id": response["output"]["responseMetadata"]["requestId"],
        "raw_response_object": response,
    }
    
    return {"text": text_output, "metadata": metadata}

