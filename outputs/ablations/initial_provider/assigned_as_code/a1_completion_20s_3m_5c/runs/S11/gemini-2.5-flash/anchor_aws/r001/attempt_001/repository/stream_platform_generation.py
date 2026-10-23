import boto3

def stream_platform_generation(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse_stream(
        modelId="us.amazon.nova-pro-v1:0", # Using the same model as invoke_platform_model.py
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )

    # The response stream yields events. Iterate through them to get the chunks.
    for event in response["stream"]:
        if "contentBlockDelta" in event:
            if "text" in event["contentBlockDelta"]["delta"]:
                yield {"chunk": event["contentBlockDelta"]["delta"]["text"], "raw_event": event}
        elif "messageStart" in event:
            yield {"chunk": "", "raw_event": event} # Indicate start of message
        elif "messageStop" in event:
            yield {"chunk": "", "raw_event": event} # Indicate end of message
