import boto3


def log_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    model_id = config.get("model_id", "amazon.titan-embed-text-v1")
    body = {"inputText": payload.get("text", "")}
    response = client.invoke_model(modelId=model_id, body=bytes(str(body).replace("'", '"'), "utf-8"), contentType="application/json", accept="application/json")
    return {"model_id": model_id, "embedding_response": response.get("body")}
