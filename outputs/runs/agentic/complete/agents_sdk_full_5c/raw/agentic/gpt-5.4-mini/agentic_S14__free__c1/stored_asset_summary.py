from __future__ import annotations

import os

import boto3

from storage_client import normalize_boto_error
from storage_models import SummaryResult


bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")


def stored_asset_summary(object_key: str, extracted_text: str) -> dict:
    prompt = f"Summarize the following asset text in 3 concise bullet points and one short paragraph. Object: {object_key}\n\n{extracted_text}"
    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=(
                "{" 
                f'"anthropic_version":"bedrock-2023-05-31","max_tokens":400,'
                f'"messages":[{{"role":"user","content":[{{"type":"text","text":{prompt!r}}}]}}]'
                "}"
            ).encode("utf-8"),
            accept="application/json",
            contentType="application/json",
        )
        body = response["body"].read().decode("utf-8")
        result = SummaryResult(object_key=object_key, summary=body, bullets=None)
        return result.to_dict()
    except Exception as exc:
        return {"error": normalize_boto_error(exc), "model_id": MODEL_ID}
