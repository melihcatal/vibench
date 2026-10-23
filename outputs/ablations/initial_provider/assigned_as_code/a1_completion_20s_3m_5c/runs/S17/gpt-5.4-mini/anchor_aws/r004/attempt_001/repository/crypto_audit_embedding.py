import boto3


def crypto_audit_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    body = {"inputText": payload.get("notes", "")}
    response = client.invoke_model(modelId=config.get("model_id", "amazon.titan-embed-text-v1"), body=str(body).encode())
    return {"embedding": response.get("body")}
