import boto3


def ocr_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    model_id = config.get("model_id", "amazon.titan-embed-text-v2:0")
    text = payload.get("text", "")
    response = client.invoke_model(
        modelId=model_id,
        body=("{\"inputText\": \"" + text.replace("\\", "\\\\").replace('"', '\\"') + "\"}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return {"embedding_response": response, "model_id": model_id}
