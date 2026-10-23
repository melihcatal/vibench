import boto3


def log_embedding(texts, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    model_id = config.get("model_id", "amazon.titan-embed-text-v2:0")
    embeddings = []
    for text in texts:
        response = client.invoke_model(body=("{\"inputText\": \"" + text.replace("\\", "\\\\").replace('"', '\\"') + "\"}"), modelId=model_id, accept="application/json", contentType="application/json")
        body = response["body"].read().decode("utf-8")
        embeddings.append({"text": text, "model_id": model_id, "raw": body})
    return {"embeddings": embeddings}
