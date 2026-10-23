import boto3


def incident_summary(findings, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = config.get("prompt", "Summarize these incident findings for review:\n" + "\n".join(str(item) for item in findings))
    response = client.converse(
        modelId=config.get("model_id", "anthropic.claude-3-haiku-20240307-v1:0"),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = response["output"]["message"]["content"][0]["text"]
    return {"summary": text}
