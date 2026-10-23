import boto3


def stored_asset_summary(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    body = {"anthropic_version": "bedrock-2023-05-31", "max_tokens": 300, "messages": [{"role": "user", "content": payload["text"]}]}
    response = client.invoke_model(modelId=config.get("model_id", "anthropic.claude-3-haiku-20240307-v1:0"), body=bytes(str(body).replace("'", '"'), "utf-8"), contentType="application/json", accept="application/json")
    return {"summary": response["body"].read().decode("utf-8")}
