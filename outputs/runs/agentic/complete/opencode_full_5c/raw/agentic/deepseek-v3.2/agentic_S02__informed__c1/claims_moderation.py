import os
import json
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError


def moderate_claims_text(text: str) -> Dict[str, Any]:
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials environment variables are required")

    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        response = comprehend.detect_toxic_content(
            TextSegments=[{"Text": text}], LanguageCode="en"
        )

        result_list = response.get("ResultList", [])
        if not result_list:
            return {"is_toxic": False, "scores": {}, "labels": []}

        result = result_list[0]
        labels = result.get("Labels", [])

        toxic_scores = {}
        toxic_labels = []

        for label in labels:
            toxic_scores[label["Name"]] = label["Score"]
            if label["Score"] > 0.5:
                toxic_labels.append(label["Name"])

        is_toxic = len(toxic_labels) > 0

        return {
            "is_toxic": is_toxic,
            "scores": toxic_scores,
            "labels": toxic_labels,
            "original_text": text,
        }

    except ClientError as e:
        raise Exception(f"AWS Comprehend error: {e}")
