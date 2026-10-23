import boto3
import os
from typing import Optional


class SecurityClient:
    def __init__(self, key_id: Optional[str] = None):
        self.key_id = key_id or os.getenv("AWS_KMS_KEY_ID")
        if not self.key_id:
            raise ValueError("AWS_KMS_KEY_ID environment variable must be set")
        self.kms = boto3.client("kms")
