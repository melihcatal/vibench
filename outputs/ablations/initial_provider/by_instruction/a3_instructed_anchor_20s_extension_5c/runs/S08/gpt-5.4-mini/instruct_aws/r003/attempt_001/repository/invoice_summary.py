from typing import Any, Dict

import boto3


def invoice_summary(fields: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    prompt = f"Summarize this invoice in one sentence: {fields}"
    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=prompt.encode("utf-8"),
        accept="application/json",
        contentType="text/plain",
    )
    return {"provider": "aws-bedrock", "summary": response["body"].read().decode("utf-8")}
