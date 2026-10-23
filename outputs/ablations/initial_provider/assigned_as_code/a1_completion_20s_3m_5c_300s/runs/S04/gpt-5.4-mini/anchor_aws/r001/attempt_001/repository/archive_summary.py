import boto3


def archive_summary(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = payload["text"]
    response = client.invoke_model(
        modelId=config.get("model_id", "anthropic.claude-3-haiku-20240307-v1:0"),
        body=f'{{"messages":[{{"role":"user","content":[{{"type":"text","text":"Summarize this transcript: {prompt}"}}]}}]}}',
        contentType="application/json",
        accept="application/json",
    )
    return {"summary": response["body"].read().decode("utf-8")}
