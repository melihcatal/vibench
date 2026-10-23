from __future__ import annotations

import json

from messaging_client import bedrock_runtime_client
from messaging_models import ProcessingSummary


def summarize_message_processing(summary: ProcessingSummary, notes: list[str]) -> str:
    prompt = (
        "Summarize pub/sub processing results in two concise sentences. "
        f"Metrics: total={summary.total}, succeeded={summary.succeeded}, "
        f"failed={summary.failed}, dead_lettered={summary.dead_lettered}. "
        f"Notes: {json.dumps(notes, ensure_ascii=False)}"
    )
    response = bedrock_runtime_client().invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 180,
                "messages": [
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ],
            }
        ),
    )
    payload = json.loads(response["body"].read())
    content = payload.get("content", [])
    return "".join(part.get("text", "") for part in content).strip()
