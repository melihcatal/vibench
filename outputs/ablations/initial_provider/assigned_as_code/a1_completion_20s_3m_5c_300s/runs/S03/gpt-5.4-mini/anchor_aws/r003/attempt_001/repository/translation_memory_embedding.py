import boto3


def translation_memory_embedding(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=(payload["text"] if isinstance(payload["text"], str) else str(payload["text"])).encode("utf-8"),
        contentType="text/plain",
        accept="application/json",
    )
    return {"embedding_response": response.get("body").read()}
