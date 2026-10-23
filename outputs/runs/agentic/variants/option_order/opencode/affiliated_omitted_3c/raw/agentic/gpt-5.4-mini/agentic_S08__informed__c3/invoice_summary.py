import boto3


def invoice_summary(invoice_fields: dict):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    prompt = f"Summarize this invoice in one sentence: {invoice_fields}"
    response = client.invoke_model(
        modelId="amazon.nova-lite-v1:0", body=prompt.encode()
    )
    return response.get("body").read().decode() if response.get("body") else ""
