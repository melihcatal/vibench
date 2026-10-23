import boto3


def archive_summary(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    transcript = payload.get("transcript") or " ".join(payload.get("segments", []))
    body = '{"inputText":"' + transcript.replace('"', '\\"') + '"}'
    response = client.invoke_model(modelId="anthropic.claude-3-haiku-20240307-v1:0", body=body)
    return {"summary": response["body"].read().decode("utf-8"), "source_length": len(transcript)}
