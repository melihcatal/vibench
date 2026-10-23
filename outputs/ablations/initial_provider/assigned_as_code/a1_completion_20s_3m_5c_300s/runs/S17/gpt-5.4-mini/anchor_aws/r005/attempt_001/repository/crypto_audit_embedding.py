import boto3


def crypto_audit_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    body = {"inputText": payload["text"]}
    response = client.invoke_model(modelId="amazon.titan-embed-text-v1", body=str(body).encode("utf-8"))
    return {"embedding": response["body"].read()}
