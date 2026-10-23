import boto3


def incident_summary(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    messages = payload.get("findings", [])
    prompt = "Summarize these error-log findings for incident review:\n" + "\n".join(str(item) for item in messages)
    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        contentType="application/json",
        accept="application/json",
        body=("{\"anthropic_version\":\"bedrock-2023-05-31\",\"max_tokens\":256,\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":%r}]}]}" % prompt).encode("utf-8"),
    )
    return {"summary": response.get("body").read().decode("utf-8")}
