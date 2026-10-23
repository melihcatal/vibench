from typing import Any, Dict, List

import boto3


class S3Request:
    def __init__(self, bucket_name: str, key: str):
        self.bucket_name = bucket_name
        self.key = key


class S3Response:
    def __init__(self, content: bytes):
        self.content = content


def normalize_s3_response(response: Dict[str, Any]) -> S3Response:
    return S3Response(response['Body'].read())


def get_object(request: S3Request) -> S3Response:
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=request.bucket_name, Key=request.key)
    return normalize_s3_response(response)