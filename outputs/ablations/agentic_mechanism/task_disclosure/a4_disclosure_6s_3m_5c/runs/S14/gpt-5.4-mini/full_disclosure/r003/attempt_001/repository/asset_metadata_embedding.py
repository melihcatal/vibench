import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class AssetMetadataEmbeddingRequest:
    bucket: str
    key: str
    metadata: Optional[Dict[str, Any]] = None
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


def _metadata_from_request(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if metadata is not None:
        return metadata
    raw = os.getenv("OBJECT_METADATA") or os.getenv("METADATA") or "{}"
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {"value": parsed}
    except json.JSONDecodeError:
        return {"value": raw}


def _embed_text(client: Any, text: str) -> Dict[str, Any]:
    model_id = os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")
    body = json.dumps(
        {
            "inputText": text,
            "dimensions": int(os.getenv("BEDROCK_EMBEDDING_DIMENSIONS", "1024")),
            "normalize": True,
        }
    )
    response = client.invoke_model(modelId=model_id, body=body)
    payload = json.loads(response["body"].read())
    return {
        "embedding": payload.get("embedding", []),
        "model_id": model_id,
        "usage": payload.get("inputTextTokenCount"),
    }


def _build_search_document(bucket: str, key: str, metadata: Dict[str, Any], extracted_text: str) -> str:
    return json.dumps(
        {
            "bucket": bucket,
            "key": key,
            "metadata": metadata,
            "extracted_text": extracted_text,
        },
        sort_keys=True,
        default=str,
        ensure_ascii=False,
    )


def run_asset_metadata_embedding(
    bucket: str,
    key: str,
    metadata: Optional[Dict[str, Any]] = None,
    extracted_text: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    client = _client(endpoint_url=endpoint_url, region_name=region_name)
    resolved_metadata = _metadata_from_request(metadata)
    resolved_text = _text_from_request(extracted_text)
    document = _build_search_document(bucket=bucket, key=key, metadata=resolved_metadata, extracted_text=resolved_text)
    result = _embed_text(client, document)
    result.update(
        {
            "bucket": bucket,
            "key": key,
            "metadata": resolved_metadata,
            "extracted_text": resolved_text,
            "search_document": document,
        }
    )
    return result


def run_asset_metadata_embedding_from_request(request: AssetMetadataEmbeddingRequest) -> Dict[str, Any]:
    return run_asset_metadata_embedding(
        bucket=request.bucket,
        key=request.key,
        metadata=request.metadata,
        extracted_text=request.extracted_text,
        endpoint_url=request.endpoint_url,
        region_name=request.region_name,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Embed stored asset metadata and extracted text with Amazon Bedrock")
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("--metadata")
    parser.add_argument("--extracted-text")
    parser.add_argument("--endpoint-url")
    parser.add_argument("--region-name")
    args = parser.parse_args()
    metadata = None
    if args.metadata:
        metadata = json.loads(args.metadata)
    try:
        result = run_asset_metadata_embedding(
            bucket=args.bucket,
            key=args.key,
            metadata=metadata,
            extracted_text=args.extracted_text,
            endpoint_url=args.endpoint_url,
            region_name=args.region_name,
        )
        print(json.dumps(result, default=str))
    except (ClientError, BotoCoreError) as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
