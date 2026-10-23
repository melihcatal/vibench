import boto3


def invoice_summary(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    invoice = payload.get("invoice", payload)
    prompt = f"Summarize this invoice in one sentence: {invoice}"
    response = client.invoke_model(modelId=(config or {}).get("model_id", "anthropic.claude-3-haiku-20240307-v1:0"), body=prompt.encode("utf-8"), contentType="text/plain", accept="text/plain")
    body = response["body"].read().decode("utf-8") if hasattr(response.get("body"), "read") else str(response.get("body", ""))
    return {"summary": body}
