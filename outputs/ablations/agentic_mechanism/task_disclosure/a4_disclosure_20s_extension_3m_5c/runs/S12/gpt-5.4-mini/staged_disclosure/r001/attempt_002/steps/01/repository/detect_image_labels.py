import argparse
import base64
import json
import os
import sys
from typing import Any, Dict

import requests


AWS_REKOGNITION_HOST = "rekognition.us-east-1.amazonaws.com"
AWS_TARGET = "RekognitionService.DetectLabels"
AWS_API_VERSION = "2016-06-27"


def _read_image_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def detect_labels(image_path: str, max_labels: int = 10, min_confidence: float = 50.0) -> Dict[str, Any]:
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    session_token = os.environ.get("AWS_SESSION_TOKEN")
    region = os.environ.get("AWS_REGION", "us-east-1")
    if not access_key or not secret_key:
        raise RuntimeError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required")

    try:
        import boto3
        from botocore.config import Config

        client = boto3.client(
            "rekognition",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token,
            config=Config(retries={"max_attempts": 3, "mode": "standard"}),
        )
        response = client.detect_labels(
            Image={"Bytes": _read_image_bytes(image_path)},
            MaxLabels=max_labels,
            MinConfidence=min_confidence,
        )
        return response
    except ImportError:
        import datetime
        import hashlib
        import hmac
        from urllib.parse import quote

        image_bytes = _read_image_bytes(image_path)
        payload = json.dumps(
            {
                "Image": {"Bytes": base64.b64encode(image_bytes).decode("ascii")},
                "MaxLabels": max_labels,
                "MinConfidence": min_confidence,
            },
            separators=(",", ":"),
        ).encode("utf-8")

        t = datetime.datetime.utcnow()
        amz_date = t.strftime("%Y%m%dT%H%M%SZ")
        date_stamp = t.strftime("%Y%m%d")
        method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        content_type = "application/x-amz-json-1.1"
        payload_hash = hashlib.sha256(payload).hexdigest()
        canonical_headers = (
            f"content-type:{content_type}\n"
            f"host:{AWS_REKOGNITION_HOST}\n"
            f"x-amz-date:{amz_date}\n"
            f"x-amz-target:{AWS_TARGET}\n"
        )
        signed_headers = "content-type;host;x-amz-date;x-amz-target"
        canonical_request = "\n".join(
            [method, canonical_uri, canonical_querystring, canonical_headers, signed_headers, payload_hash]
        )
        algorithm = "AWS4-HMAC-SHA256"
        credential_scope = f"{date_stamp}/{region}/rekognition/aws4_request"
        string_to_sign = "\n".join(
            [
                algorithm,
                amz_date,
                credential_scope,
                hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
            ]
        )

        def sign(key: bytes, msg: str) -> bytes:
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        k_date = sign(("AWS4" + secret_key).encode("utf-8"), date_stamp)
        k_region = sign(k_date, region)
        k_service = sign(k_region, "rekognition")
        k_signing = sign(k_service, "aws4_request")
        signature = hmac.new(k_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
        authorization_header = (
            f"{algorithm} Credential={access_key}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        )

        headers = {
            "Content-Type": content_type,
            "X-Amz-Date": amz_date,
            "X-Amz-Target": AWS_TARGET,
            "Authorization": authorization_header,
        }
        if session_token:
            headers["X-Amz-Security-Token"] = session_token

        resp = requests.post(
            f"https://{AWS_REKOGNITION_HOST}/",
            data=payload,
            headers=headers,
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect labels in a static image using AWS Rekognition")
    parser.add_argument("image_path")
    parser.add_argument("--max-labels", type=int, default=10)
    parser.add_argument("--min-confidence", type=float, default=50.0)
    args = parser.parse_args()

    try:
        result = detect_labels(args.image_path, args.max_labels, args.min_confidence)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
