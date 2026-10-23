import boto3


def secret_audit_embedding(secret_id: str, note: str, region_name: str | None = None) -> dict:
    client = boto3.client("bedrock-runtime", region_name=region_name)
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=("{" + f'"inputText":"{note}"' + "}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return {"secret_id": secret_id, "embedding": response["body"].read()}
