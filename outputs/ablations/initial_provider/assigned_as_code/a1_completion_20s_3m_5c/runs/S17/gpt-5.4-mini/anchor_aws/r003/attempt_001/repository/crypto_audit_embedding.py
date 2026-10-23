import boto3


def crypto_audit_embedding(payload, config=None):
    config = config or {}
    bedrock = boto3.client("bedrock-runtime", region_name=config.get("region"))
    text = payload.get("notes", "")
    response = bedrock.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v1"),
        body=(f'{"inputText": "{text}"}').encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    return {"embedding": response["body"].read()}
