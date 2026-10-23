import boto3


def transcript_embedding(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    response = client.invoke_model(
        modelId=payload.get("model_id", "amazon.titan-embed-text-v2:0"),
        body=str({"inputText": payload["text"]}),
    )
    return {"embedding": response.get("body", b"")}
