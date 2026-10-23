import os
import json
import boto3
from typing import Optional, Dict, Any


class SecurityClient:
    def __init__(self):
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        self.kms_client = None
        self._initialize_clients()

    def _initialize_clients(self):
        if self.aws_access_key_id and self.aws_secret_access_key:
            self.kms_client = boto3.client(
                "kms",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region,
            )
        else:
            self.kms_client = boto3.client("kms", region_name=self.aws_region)

    def get_kms_client(self):
        return self.kms_client

    def normalize_payload(self, payload: Any) -> bytes:
        if isinstance(payload, str):
            return payload.encode("utf-8")
        elif isinstance(payload, bytes):
            return payload
        elif isinstance(payload, dict):
            return json.dumps(payload).encode("utf-8")
        else:
            return str(payload).encode("utf-8")

    def parse_encryption_response(self, response: Dict) -> Dict[str, Any]:
        return {
            "ciphertext": response.get("CiphertextBlob"),
            "key_id": response.get("KeyId"),
            "encryption_context": response.get("EncryptionContext", {}),
            "algorithm": response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        }

    def parse_decryption_response(self, response: Dict) -> Dict[str, Any]:
        return {
            "plaintext": response.get("Plaintext"),
            "key_id": response.get("KeyId"),
            "encryption_context": response.get("EncryptionContext", {}),
            "algorithm": response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        }

    def parse_signature_response(self, response: Dict) -> Dict[str, Any]:
        return {
            "signature": response.get("Signature"),
            "key_id": response.get("KeyId"),
            "signing_algorithm": response.get("SigningAlgorithm"),
            "message_type": response.get("MessageType", "RAW"),
        }

    def get_key_arn(self, key_id: str) -> str:
        if key_id.startswith("arn:aws:kms:"):
            return key_id
        elif key_id.startswith("alias/"):
            return f"arn:aws:kms:{self.aws_region}:*:key/{key_id}"
        else:
            return f"arn:aws:kms:{self.aws_region}:*:key/{key_id}"


security_client = SecurityClient()
