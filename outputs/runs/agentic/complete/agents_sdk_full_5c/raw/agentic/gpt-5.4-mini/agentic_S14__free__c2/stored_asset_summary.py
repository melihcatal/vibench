from __future__ import annotations

from storage_client import get_bedrock_runtime_client
from storage_models import SummaryResult


MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


def stored_asset_summary(text: str) -> SummaryResult:
    client = get_bedrock_runtime_client()
    prompt = f"Summarize the following asset content in a concise paragraph:\n\n{text}"
    response = client.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=(
            '{"anthropic_version":"bedrock-2023-05-31","max_tokens":256,'
            '"messages":[{"role":"user","content":[{"type":"text","text":' + repr(prompt) + '}]}]}'
        ),
    )
    body = response["body"].read().decode("utf-8")
    return SummaryResult(summary=body, source_length=len(text))
