import boto3


def platform_output_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.invoke_model(
        modelId=config.get("embedding_model_id", "amazon.titan-embed-text-v2:0"),
        body=("{\"inputText\": \"" + payload["text"].replace("\\", "\\\\").replace('"', '\\"') + "\"}").encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    body = response["body"].read().decode("utf-8")
    return {"embedding_response": body, "model_id": config.get("embedding_model_id", "amazon.titan-embed-text-v2:0")}
