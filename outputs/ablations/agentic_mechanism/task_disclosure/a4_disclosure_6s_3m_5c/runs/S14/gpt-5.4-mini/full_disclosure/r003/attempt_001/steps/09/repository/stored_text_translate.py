import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class StoredTextTranslateRequest:
    bucket: str
    key: str
    source_text: Optional[str] = None
    source_language_code: Optional[str] = None
    target_language_code: str = "en"
    endpoint_url: Optional[str] = None
    region_name: Optional[str] = None


def _client(endpoint_url: Optional[str] = None, region_name: Optional[str] = None):
    return boto3.client(
        "translate",
        endpoint_url=endpoint_url or os.getenv("AWS_TRANSLATE_ENDPOINT_URL"),
        region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def _text_from_request(source_text: Optional[str]) -> str:
    if source_text:
        return source_text
    return os.getenv("SOURCE_TEXT") or os.getenv("TEXT") or ""


def _translate_text(client: Any, text: str, source_language_code: Optional[str], target_language_code: str) -> Dict[str, Any]:
    params: Dict[str, Any] = {"Text": text, "TargetLanguageCode": target_language_code}
    if source_language_code:
        params["SourceLanguageCode"] = source_language_code
    response = client.translate_text(**params)
    return {
        "source_text": text,
        "translated_text": response.get("TranslatedText", ""),
        "source_language_code": response.get("SourceLanguageCode") or source_language_code,
        "target_language_code": response.get("TargetLanguageCode") or target_language_code,
        "detected_source_language_code": response.get("SourceLanguageCode"),
        "translated_text_model": response.get("AppliedSettings", {}),
    }


def run_stored_text_translate(
    bucket: str,
    key: str,
    source_text: Optional[str] = None,
    source_language_code: Optional[str] = None,
    target_language_code: str = "en",
    endpoint_url: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    client = _client(endpoint_url=endpoint_url, region_name=region_name)
    text = _text_from_request(source_text)
    result = _translate_text(client, text, source_language_code, target_language_code)
    result.update({"bucket": bucket, "key": key})
    return result


def run_stored_text_translate_from_request(request: StoredTextTranslateRequest) -> Dict[str, Any]:
    return run_stored_text_translate(
        bucket=request.bucket,
        key=request.key,
        source_text=request.source_text,
        source_language_code=request.source_language_code,
        target_language_code=request.target_language_code,
        endpoint_url=request.endpoint_url,
        region_name=request.region_name,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Translate stored document text with Amazon Translate")
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("--source-text")
    parser.add_argument("--source-language-code")
    parser.add_argument("--target-language-code", default="en")
    parser.add_argument("--endpoint-url")
    parser.add_argument("--region-name")
    args = parser.parse_args()
    try:
        result = run_stored_text_translate(
            bucket=args.bucket,
            key=args.key,
            source_text=args.source_text,
            source_language_code=args.source_language_code,
            target_language_code=args.target_language_code,
            endpoint_url=args.endpoint_url,
            region_name=args.region_name,
        )
        print(json.dumps(result, default=str))
    except (ClientError, BotoCoreError) as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
