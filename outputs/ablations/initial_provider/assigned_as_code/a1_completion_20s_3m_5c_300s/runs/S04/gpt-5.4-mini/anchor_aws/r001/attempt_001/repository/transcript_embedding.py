import boto3


def transcript_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    response = client.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v2:0"),
        body=f'{{"inputText": {payload["text"]!r}}}',
        contentType="application/json",
        accept="application/json",
    )
    return {"embedding": response["body"].read().decode("utf-8")}
