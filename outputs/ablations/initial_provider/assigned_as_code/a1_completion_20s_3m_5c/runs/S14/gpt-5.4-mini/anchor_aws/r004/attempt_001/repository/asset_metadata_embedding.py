import boto3


def asset_metadata_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    content = payload.get("text", "") + "\n" + str(payload.get("metadata", {}))
    response = client.invoke_model(modelId=config.get("model_id", "amazon.titan-embed-text-v2:0"), body=("{\"inputText\": " + repr(content) + "}").encode("utf-8"), contentType="application/json", accept="application/json")
    return {"embedding": response["body"].read().decode("utf-8")}
