import boto3


def invoice_summary(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    model_id = (config or {}).get("model_id", "anthropic.claude-3-haiku-20240307-v1:0")
    prompt = "Summarize this invoice in one sentence: " + str(payload.get("invoice", {}))
    response = client.converse(modelId=model_id, messages=[{"role": "user", "content": [{"text": prompt}]}])
    text = response["output"]["message"]["content"][0].get("text", "")
    return {"summary": text}
