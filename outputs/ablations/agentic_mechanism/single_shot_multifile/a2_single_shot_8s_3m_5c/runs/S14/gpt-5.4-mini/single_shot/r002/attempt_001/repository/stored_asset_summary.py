import os
import boto3
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse

AWS_BEDROCK_MODEL_ID = os.getenv("AWS_BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")


def summarize_stored_asset(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    client = boto3.client("bedrock-runtime")
    prompt = f"Summarize the following asset in {request.max_sentences} sentences. Title: {request.asset_title or 'Untitled'}\n\n{request.asset_text}"
    body = {"anthropic_version": "bedrock-2023-05-31", "max_tokens": 300, "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]}
    resp = client.invoke_model(modelId=AWS_BEDROCK_MODEL_ID, body=bytes(__import__("json").dumps(body), "utf-8"))
    data = __import__("json").loads(resp["body"].read())
    text = "".join(part.get("text", "") for part in data.get("content", []))
    return StoredAssetSummaryResponse(asset_title=request.asset_title, summary=text, provider="aws-bedrock")
