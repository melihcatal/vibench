import boto3


def translation_memory_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    text = payload["text"]
    response = client.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v1"),
        body=("{\"inputText\": \"" + text.replace("\\", "\\\\").replace('"', '\\"') + "\"}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return {
        "text": text,
        "embedding": response["body"].read(),
    }
