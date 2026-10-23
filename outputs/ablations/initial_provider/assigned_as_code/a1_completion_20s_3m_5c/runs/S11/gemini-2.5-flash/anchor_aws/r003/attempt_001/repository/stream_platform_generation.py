import boto3

def stream_platform_generation(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse_stream(
        modelId="us.amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )

    # Iterate through the stream and yield text blocks, preserving response objects
    for chunk in response["stream"]:
        if "contentBlockDelta" in chunk:
            delta = chunk["contentBlockDelta"]
            if "text" in delta:
                yield {"text": delta["text"], "_original_chunk": chunk}
        elif "messageStart" in chunk or "messageStop" in chunk or "metadata" in chunk:
            yield {"_original_chunk": chunk} # Preserve other chunks for metadata
