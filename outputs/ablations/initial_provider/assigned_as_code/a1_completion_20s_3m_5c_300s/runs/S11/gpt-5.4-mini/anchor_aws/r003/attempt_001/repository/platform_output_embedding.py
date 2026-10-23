import boto3


def platform_output_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v2:0"),
        body=("{" + f'"inputText":"{payload["text"]}"' + "}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    body = response["body"].read().decode("utf-8")
    return {"embedding": body, "modelId": config.get("model_id", "amazon.titan-embed-text-v2:0")}
