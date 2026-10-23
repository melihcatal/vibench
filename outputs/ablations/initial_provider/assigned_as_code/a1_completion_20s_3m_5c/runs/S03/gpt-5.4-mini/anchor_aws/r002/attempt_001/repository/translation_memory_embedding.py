import boto3


def translation_memory_embedding(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    model_id = payload.get("model_id", "amazon.titan-embed-text-v1")
    body = {"inputText": payload.get("text", "")}
    response = client.invoke_model(modelId=model_id, body=str(body).replace("'", '"'))
    return {
        "model_id": model_id,
        "embedding": response.get("body").read() if hasattr(response.get("body"), "read") else response.get("body"),
    }
