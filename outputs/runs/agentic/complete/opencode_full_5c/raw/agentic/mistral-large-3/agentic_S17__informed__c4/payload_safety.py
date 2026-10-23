import os
from typing import Union
from security_models import SafetyCheckResult
import boto3
from botocore.exceptions import ClientError


class PayloadSafetyChecker:
    def __init__(self):
        self.comprehend = boto3.client(
            "comprehend",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def check_payload_safety(self, text: Union[str, bytes]) -> SafetyCheckResult:
        if isinstance(text, bytes):
            text = text.decode("utf-8")

        try:
            response = self.comprehend.detect_toxic_content(
                TextSegments=[{"Text": text}], LanguageCode="en"
            )

            violations = {}
            for result in response.get("ResultList", []):
                for label in result.get("Labels", []):
                    if label["Score"] > 0.5:
                        violations[label["Name"]] = label["Score"]

            return SafetyCheckResult(
                is_safe=len(violations) == 0,
                violations=violations,
                confidence=1.0 - max(violations.values()) if violations else 1.0,
            )
        except ClientError as e:
            raise Exception(f"AWS Comprehend toxicity detection failed: {e}")
