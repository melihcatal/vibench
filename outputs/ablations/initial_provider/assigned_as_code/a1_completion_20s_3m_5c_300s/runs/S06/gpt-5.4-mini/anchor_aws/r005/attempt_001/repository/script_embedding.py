import boto3


def script_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    body = {"inputText": payload["text"]}
    response = client.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v2:0"),
        body=str(body).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    return {"embedding": response["body"].read()}
