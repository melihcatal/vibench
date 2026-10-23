import boto3


def asset_metadata_embedding(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    model_id = payload.get("model_id", "amazon.titan-embed-text-v2:0")
    text = payload.get("text", "")
    return client.invoke_model(
        modelId=model_id,
        body=bytes('{"inputText":"' + text.replace('"', '\\"') + '"}', "utf-8"),
    )
