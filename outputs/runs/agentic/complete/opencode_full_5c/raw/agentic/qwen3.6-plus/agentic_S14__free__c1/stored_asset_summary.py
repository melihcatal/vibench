from __future__ import annotations

import json
from typing import Optional

from storage_client import get_bedrock_runtime_client, get_object_content, get_s3_client
from storage_models import SummaryRequest, SummaryResponse, normalize_summary_response

CLAUDE_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

SYSTEM_PROMPT = (
    "You are a helpful assistant that summarizes documents and assets. "
    "Provide a concise, accurate summary that captures the key points and main ideas. "
    "Focus on factual content and important details."
)


def summarize_stored_asset(
    bucket: str,
    key: str,
    max_tokens: int = 500,
    temperature: float = 0.3,
    version_id: Optional[str] = None,
    bedrock_client=None,
    s3_client=None,
) -> SummaryResponse:
    if s3_client is None:
        s3_client = get_s3_client()
    if bedrock_client is None:
        bedrock_client = get_bedrock_runtime_client()

    document_bytes = get_object_content(bucket, key, version_id, client=s3_client)
    text_content = document_bytes.decode("utf-8", errors="replace")

    request = SummaryRequest(
        text=text_content,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    prompt = f"<system>{SYSTEM_PROMPT}</system><user>Summarize the following document:\n\n{text_content}</user>"

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": SYSTEM_PROMPT,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Summarize the following document:\n\n{text_content}",
                        }
                    ],
                }
            ],
        }
    )

    response = bedrock_client.invoke_model(
        modelId=CLAUDE_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    return normalize_summary_response(response, CLAUDE_MODEL_ID)


def summarize_text_content(
    text: str,
    max_tokens: int = 500,
    temperature: float = 0.3,
    bedrock_client=None,
) -> SummaryResponse:
    if bedrock_client is None:
        bedrock_client = get_bedrock_runtime_client()

    request = SummaryRequest(
        text=text,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": SYSTEM_PROMPT,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Summarize the following content:\n\n{text}",
                        }
                    ],
                }
            ],
        }
    )

    response = bedrock_client.invoke_model(
        modelId=CLAUDE_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    return normalize_summary_response(response, CLAUDE_MODEL_ID)
