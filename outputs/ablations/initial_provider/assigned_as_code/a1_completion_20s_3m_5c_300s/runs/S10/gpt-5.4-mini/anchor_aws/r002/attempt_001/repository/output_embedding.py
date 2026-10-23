import boto3


def output_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    response = client.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v2:0"),
        body=("{\"inputText\":\"" + payload["text"].replace("\\", "\\\\").replace('"', '\\"') + "\"}").encode(),
        accept="application/json",
        contentType="application/json",
    )
    body = response["body"].read().decode()
    return {"embedding": __import__("json").loads(body)["embedding"]}
