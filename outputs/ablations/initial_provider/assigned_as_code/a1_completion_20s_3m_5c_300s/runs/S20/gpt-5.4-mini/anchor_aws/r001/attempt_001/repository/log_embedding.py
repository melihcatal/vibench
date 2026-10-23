import boto3


def log_embedding(texts, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    model_id = config.get("model_id", "amazon.titan-embed-text-v1")
    vectors = []
    for text in texts:
        response = client.invoke_model(
            modelId=model_id,
            body=("{\"inputText\": \"" + text.replace("\\", "\\\\").replace('"', '\\"') + "\"}").encode("utf-8"),
            contentType="application/json",
            accept="application/json",
        )
        vectors.append(response["body"].read())
    return {"model_id": model_id, "embeddings": vectors}
