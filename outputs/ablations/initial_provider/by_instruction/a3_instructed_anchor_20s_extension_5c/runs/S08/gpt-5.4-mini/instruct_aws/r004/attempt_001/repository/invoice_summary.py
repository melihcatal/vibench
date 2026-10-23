from typing import Any, Dict

import boto3


def invoice_summary(extracted_invoice: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    prompt = f"Summarize this invoice: {extracted_invoice}"
    response = client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        body=("{" + f'"prompt": {prompt!r}' + "}").encode(),
        accept="application/json",
        contentType="application/json",
    )
    return {"provider": "aws_bedrock", "response": response}
