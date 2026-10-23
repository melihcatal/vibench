from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class DocumentClientConfig:
    aws_region: str
    invoice_model_id: str
    receipt_model_id: str
    summary_model_id: str
    moderation_model_id: str
    translation_model_id: str


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        invoice_model_id=os.getenv("BEDROCK_INVOICE_MODEL_ID", "amazon.nova-lite-v1:0"),
        receipt_model_id=os.getenv("BEDROCK_RECEIPT_MODEL_ID", "amazon.nova-lite-v1:0"),
        summary_model_id=os.getenv("BEDROCK_SUMMARY_MODEL_ID", "amazon.nova-lite-v1:0"),
        moderation_model_id=os.getenv("BEDROCK_MODERATION_MODEL_ID", "amazon.nova-micro-v1:0"),
        translation_model_id=os.getenv("BEDROCK_TRANSLATION_MODEL_ID", "amazon.nova-lite-v1:0"),
    )


def bedrock_runtime(region_name: Optional[str] = None):
    cfg = load_config()
    return boto3.client("bedrock-runtime", region_name=region_name or cfg.aws_region)


def invoke_bedrock_json(model_id: str, prompt: str, *, region_name: Optional[str] = None) -> Dict[str, Any]:
    client = bedrock_runtime(region_name)
    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ],
        inferenceConfig={"maxTokens": 1024, "temperature": 0.0},
    )
    text = response["output"]["message"]["content"][0]["text"]
    return {"raw_text": text, "response": response}


def invoke_bedrock_text(model_id: str, prompt: str, *, region_name: Optional[str] = None) -> str:
    return invoke_bedrock_json(model_id, prompt, region_name=region_name)["raw_text"]
