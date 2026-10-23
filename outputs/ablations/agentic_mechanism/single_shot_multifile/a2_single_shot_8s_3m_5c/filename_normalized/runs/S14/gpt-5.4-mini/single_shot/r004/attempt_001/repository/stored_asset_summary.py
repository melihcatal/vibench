from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from storage_models import StoredAssetSummaryResult

BEDROCK_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


def summarize_stored_asset(text: str, bucket: str, key: str, content_type: Optional[str] = None) -> StoredAssetSummaryResult:
    client = boto3.client("bedrock-runtime")
    prompt = f"Summarize the following asset content in 3-5 concise bullet points:\n\n{text}"
    try:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        }
        response = client.invoke_model(modelId=BEDROCK_MODEL_ID, body=__import__("json").dumps(body))
        payload = __import__("json").loads(response["body"].read())
        summary = ""
        for block in payload.get("content", []):
            if block.get("type") == "text":
                summary += block.get("text", "")
        return StoredAssetSummaryResult(bucket=bucket, key=key, summary=summary.strip(), content_type=content_type)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"asset summarization failed with {BEDROCK_MODEL_ID}: {exc}") from exc


__all__ = ["summarize_stored_asset"]
