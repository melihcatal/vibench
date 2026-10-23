import boto3


def log_embedding(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    body = "{\"inputText\":%r}" % payload["text"]
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        contentType="application/json",
        accept="application/json",
        body=body.encode("utf-8"),
    )
    return {"embedding": response.get("body").read().decode("utf-8")}
