import boto3


def translation_memory_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    body = {"inputText": payload["text"]}
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=str(body).replace("'", '"').encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return {
        "text": payload["text"],
        "embedding": response["body"].read(),
    }
