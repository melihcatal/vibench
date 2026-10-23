import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class StoredAssetSummaryRequest:
    bucket: str
    key: str
    extracted_text: Optional[str] = None
    endpoint_url: Optional[str] = None
    region_name: Optional[str] = None


def _client(endpoint_url: Optional[str] = None, region_name: Optional[str] = None):
    return boto3.client(
        "bedrock-runtime",
        endpoint_url=endpoint_url or os.getenv("AWS_BEDROCK_RUNTIME_ENDPOINT_URL"),
        region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def _text_from_request(extracted_text: Optional[str]) -> str:
    if extracted_text:
        return extracted_text
    return os.getenv("EXTRACTED_TEXT") or os.getenv("TEXT") or ""


def _summarize_text(client: Any, text: str) -> Dict[str, Any]:
    model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 400,
            "temperature": 0,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Summarize the following extracted asset content in a concise, factual way:\n\n{text}",
                        }
                    ],
                }
            ],
        }
    )
    response = client.invoke_model(modelId=model_id, body=body)
    payload = json.loads(response["body"].read())
    summary = ""
    content = payload.get("content") or []
    if content:
        summary = "".join(part.get("text", "") for part in content if isinstance(part, dict))
    return {
        "summary": summary,
        "model_id": model_id,
        "usage": payload.get("usage", {}),
        "stop_reason": payload.get("stop_reason"),
    }


def run_stored_asset_summary(
    bucket: str,
    key: str,
    extracted_text: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    client = _client(endpoint_url=endpoint_url, region_name=region_name)
    text = _text_from_request(extracted_text)
    result = _summarize_text(client, text)
    result.update({"bucket": bucket, "key": key, "extracted_text": text})
    return result


def run_stored_asset_summary_from_request(request: StoredAssetSummaryRequest) -> Dict[str, Any]:
    return run_stored_asset_summary(
        bucket=request.bucket,
        key=request.key,
        extracted_text=request.extracted_text,
        endpoint_url=request.endpoint_url,
        region_name=request.region_name,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Summarize stored asset content with Amazon Bedrock")
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("--extracted-text")
    parser.add_argument("--endpoint-url")
    parser.add_argument("--region-name")
    args = parser.parse_args()
    try:
        result = run_stored_asset_summary(
            bucket=args.bucket,
            key=args.key,
            extracted_text=args.extracted_text,
            endpoint_url=args.endpoint_url,
            region_name=args.region_name,
        )
        print(json.dumps(result, default=str))
    except (ClientError, BotoCoreError) as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
