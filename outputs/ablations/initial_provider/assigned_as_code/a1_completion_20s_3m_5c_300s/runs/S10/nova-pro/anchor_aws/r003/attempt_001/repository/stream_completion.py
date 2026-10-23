import boto3


def stream_completion(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = payload["text"]
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        stream=True,
    )
    for event in response['events']:
        if 'message' in event:
            yield event['message']['content'][0]['text']
        else:
            yield ''