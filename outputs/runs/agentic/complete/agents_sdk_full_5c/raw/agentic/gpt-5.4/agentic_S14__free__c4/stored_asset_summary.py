from __future__ import annotations

import json

from storage_client import get_bedrock_runtime_client
from storage_models import SummaryResult


BEDROCK_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


def summarize_asset_text(text: str, max_tokens: int = 300) -> SummaryResult:
    bedrock = get_bedrock_runtime_client()
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Summarize the following extracted asset content in concise bullet points:\n\n" + text,
                    }
                ],
            }
        ],
    }
    response = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )
    payload = json.loads(response["body"].read())
    summary = "\n".join(part["text"] for part in payload.get("content", []) if part.get("type") == "text")
    return SummaryResult(summary=summary, model=BEDROCK_MODEL_ID)
