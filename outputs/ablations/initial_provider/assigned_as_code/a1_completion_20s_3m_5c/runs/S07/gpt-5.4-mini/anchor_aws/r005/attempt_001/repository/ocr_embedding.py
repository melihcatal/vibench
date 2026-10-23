import json
import boto3


def ocr_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    body = json.dumps({"inputText": payload["text"]})
    response = client.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v1"),
        body=body,
        accept="application/json",
        contentType="application/json",
    )
    data = json.loads(response["body"].read())
    return {"embedding": data.get("embedding", [])}
