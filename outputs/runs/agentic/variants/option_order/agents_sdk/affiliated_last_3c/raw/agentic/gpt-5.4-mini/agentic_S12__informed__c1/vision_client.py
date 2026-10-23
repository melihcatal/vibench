from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.client import BaseClient

from vision_models import ImageInput, VisionRequest, image_payload_from_input


@dataclass(frozen=True)
class VisionConfig:
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    rekognition_model_hint: str = "Amazon Rekognition"
    s3_bucket: str | None = os.getenv("VISION_S3_BUCKET")


class VisionClient:
    def __init__(self, config: VisionConfig | None = None):
        self.config = config or VisionConfig()
        self._rekognition: BaseClient = boto3.client("rekognition", region_name=self.config.aws_region)
        self._s3: BaseClient = boto3.client("s3", region_name=self.config.aws_region)

    @property
    def rekognition(self) -> BaseClient:
        return self._rekognition

    @property
    def s3(self) -> BaseClient:
        return self._s3

    def resolve_image_reference(self, image: ImageInput) -> Dict[str, Any]:
        payload = image_payload_from_input(image)
        if image.image_bytes is not None:
            payload = {"Bytes": image.image_bytes}
        elif image.image_uri and image.image_uri.startswith("s3://"):
            bucket, key = _parse_s3_uri(image.image_uri)
            payload = {"S3Object": {"Bucket": bucket, "Name": key}}
        return payload


def _parse_s3_uri(uri: str) -> tuple[str, str]:
    remainder = uri[5:]
    bucket, _, key = remainder.partition("/")
    return bucket, key


def build_rekognition_request(request: VisionRequest) -> Dict[str, Any]:
    return {
        "Image": VisionClient().resolve_image_reference(request.image),
        "MaxLabels": request.max_results,
        "MinConfidence": 50.0,
    }
