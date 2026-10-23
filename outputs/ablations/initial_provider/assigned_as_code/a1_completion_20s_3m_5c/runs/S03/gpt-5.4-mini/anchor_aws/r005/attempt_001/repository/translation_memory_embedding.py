import boto3


def translation_memory_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    body = '{"inputText":"' + payload.get("text", "").replace('"', '\\"') + '"}'
    response = client.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v1"),
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    return {"embedding": response.get("body")}
