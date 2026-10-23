import boto3

from storage_client import load_storage_config


def asset_metadata_embedding(payload, config=None):
    cfg = load_storage_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    model_id = payload.get("model_id", "amazon.titan-embed-text-v2:0")
    metadata = payload.get("metadata", {})
    text = payload.get("text", "")
    source = str(metadata) + "\n" + text
    response = client.invoke_model(
        modelId=model_id,
        body=bytes('{"inputText": "' + source.replace('"', '\\"') + '"}', "utf-8"),
    )
    return {"model_id": model_id, "embedding": response.get("body")}
