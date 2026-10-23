import boto3


def log_embedding(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    response = client.invoke_model(
        modelId=payload.get("model_id", "amazon.titan-embed-text-v1"),
        body=("{\"inputText\": \"" + payload["text"].replace("\\", "\\\\").replace('"', '\\"') + "\"}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return {"embedding": response["body"].read().decode("utf-8")}
