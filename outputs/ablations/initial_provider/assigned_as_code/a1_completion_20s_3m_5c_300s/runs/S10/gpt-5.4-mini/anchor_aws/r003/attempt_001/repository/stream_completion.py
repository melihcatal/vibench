import boto3

from model_client import get_model_id, load_config


def stream_completion(payload, config=None):
    config = load_config(config)
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    response = client.converse_stream(
        modelId=get_model_id(config),
        messages=[{"role": "user", "content": [{"text": payload["prompt"]}]}],
    )
    chunks = []
    for event in response["stream"]:
        if "contentBlockDelta" in event and "delta" in event["contentBlockDelta"]:
            delta = event["contentBlockDelta"]["delta"]
            if "text" in delta:
                chunks.append(delta["text"])
    return {"text": "".join(chunks)}
