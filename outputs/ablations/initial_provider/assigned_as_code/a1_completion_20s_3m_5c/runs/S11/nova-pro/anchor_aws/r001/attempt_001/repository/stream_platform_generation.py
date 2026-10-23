import boto3

def stream_platform_generation(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse(
        modelId="us.amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
        stream=True,
    )
    for event in response['events']:
        if 'text' in event['message']['content'][0]:
            yield event['message']['content'][0]['text']
        else:
            yield ""