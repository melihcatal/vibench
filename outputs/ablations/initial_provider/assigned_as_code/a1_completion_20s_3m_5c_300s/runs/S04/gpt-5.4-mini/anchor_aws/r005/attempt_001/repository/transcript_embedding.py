import boto3


def transcript_embedding(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    text = payload.get("text") or " ".join(segment.get("text", "") for segment in payload.get("segments", []))
    response = client.invoke_model(modelId="amazon.titan-embed-text-v1", body='{"inputText":"' + text.replace('"', '\\"') + '"}')
    return {"embedding": response["body"].read().decode("utf-8"), "text": text}
