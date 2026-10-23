import boto3


def output_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    response = client.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v2:0"),
        body=(payload["text"] if isinstance(payload, dict) and "text" in payload else str(payload)).encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    body = response["body"].read().decode("utf-8")
    return {"text": body}
