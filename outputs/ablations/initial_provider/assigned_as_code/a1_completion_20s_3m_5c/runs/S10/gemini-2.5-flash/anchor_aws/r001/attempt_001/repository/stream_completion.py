import boto3


def stream_completion(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = payload["prompt"]
    response_stream = client.converse_stream(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 1024},
    )
    
    # In a real scenario, you would iterate and yield tokens.
    # For this exercise, we will just return the first chunk or an empty string.
    # The Bedrock streaming API returns an iterator over dictionaries.
    # Each dictionary could contain different types of events.
    # We are interested in 'contentBlockDelta' event for streaming text.
    
    for event in response_stream["stream"]:
        if "contentBlockDelta" in event:
            if "text" in event["contentBlockDelta"]["delta"]:
                yield event["contentBlockDelta"]["delta"]["text"]
