import boto3


def crypto_audit_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    body = {
        "inputText": payload["text"],
        "dimensions": config.get("dimensions", 1024),
    }
    response = client.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v1"),
        body=str(body).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    return {"embedding_response": response["body"].read()}
