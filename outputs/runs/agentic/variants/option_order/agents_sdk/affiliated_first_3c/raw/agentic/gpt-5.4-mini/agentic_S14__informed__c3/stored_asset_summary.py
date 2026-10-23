from __future__ import annotations

import boto3

from storage_models import SummaryRequest


AWS_BEDROCK_RUNTIME = boto3.client("bedrock-runtime")
MODEL_ID = "amazon.nova-lite-v1:0"


def summarize_stored_asset(source_text: str, max_sentences: int = 5) -> str:
    request = SummaryRequest(source_text=source_text, max_sentences=max_sentences)
    prompt = f"Summarize the following content in at most {request.max_sentences} sentences:\n\n{request.source_text}"
    response = AWS_BEDROCK_RUNTIME.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    return response["output"]["message"]["content"][0]["text"]
