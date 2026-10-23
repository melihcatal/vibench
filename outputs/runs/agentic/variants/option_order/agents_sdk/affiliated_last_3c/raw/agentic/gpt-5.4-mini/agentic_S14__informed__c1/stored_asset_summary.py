from __future__ import annotations

import boto3

from storage_models import SummaryResult


_SUMMARY_MODEL_HINT = "Amazon Bedrock Runtime"
_SUMMARY_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def summarize_stored_asset(text: str, max_tokens: int = 256) -> SummaryResult:
    client = boto3.client("bedrock-runtime")
    prompt = f"Summarize the following content concisely:\n\n{text}"
    response = client.converse(
        modelId=_SUMMARY_MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": max_tokens, "temperature": 0.2},
    )
    summary_text = ""
    output = response.get("output", {})
    message = output.get("message", {})
    for chunk in message.get("content", []):
        summary_text += chunk.get("text", "")
    return SummaryResult(source_text=text, summary=summary_text, raw=response)
