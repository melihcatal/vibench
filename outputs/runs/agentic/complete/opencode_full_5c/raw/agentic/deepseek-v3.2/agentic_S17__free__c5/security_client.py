import os
import json
import base64
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError


class SecurityClient:
    """Client helper utilities for Key Management and Encryption."""

    def __init__(self, region: Optional[str] = None):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.kms_client = boto3.client("kms", region_name=self.region)

        # Configuration
        self.encryption_key_id = os.getenv("AWS_KMS_KEY_ID", "alias/encryption-key")
        self.signing_key_id = os.getenv("AWS_KMS_SIGNING_KEY_ID", "alias/signing-key")
        self.envelope_key_id = os.getenv(
            "AWS_KMS_ENVELOPE_KEY_ID", "alias/envelope-key"
        )

    def get_key_metadata(self, key_id: Optional[str] = None) -> Dict[str, Any]:
        """Get metadata for a KMS key."""
        key_to_describe = key_id or self.encryption_key_id

        try:
            response = self.kms_client.describe_key(KeyId=key_to_describe)
            key_metadata = response["KeyMetadata"]

            return {
                "key_id": key_metadata["KeyId"],
                "arn": key_metadata["Arn"],
                "creation_date": key_metadata["CreationDate"].isoformat(),
                "description": key_metadata.get("Description", ""),
                "key_state": key_metadata["KeyState"],
                "key_usage": key_metadata["KeyUsage"],
                "key_spec": key_metadata.get("KeySpec", ""),
                "origin": key_metadata.get("Origin", ""),
                "provider": "aws_kms",
            }
        except ClientError as e:
            raise Exception(f"Failed to get key metadata: {e}")

    def list_keys(self, limit: int = 100) -> list:
        """List available KMS keys."""
        try:
            response = self.kms_client.list_keys(Limit=limit)
            keys = []

            for key in response["Keys"]:
                try:
                    key_info = self.get_key_metadata(key["KeyId"])
                    keys.append(key_info)
                except:
                    keys.append(
                        {
                            "key_id": key["KeyId"],
                            "arn": key["KeyArn"],
                            "provider": "aws_kms",
                        }
                    )

            return keys
        except ClientError as e:
            raise Exception(f"Failed to list keys: {e}")

    def generate_data_key(
        self, key_id: Optional[str] = None, key_spec: str = "AES_256"
    ) -> Dict[str, Any]:
        """Generate a data key for envelope encryption."""
        key_to_use = key_id or self.envelope_key_id

        try:
            response = self.kms_client.generate_data_key(
                KeyId=key_to_use, KeySpec=key_spec
            )

            return {
                "plaintext_key": base64.b64encode(response["Plaintext"]).decode(
                    "utf-8"
                ),
                "encrypted_key": base64.b64encode(response["CiphertextBlob"]).decode(
                    "utf-8"
                ),
                "key_id": key_to_use,
                "key_spec": key_spec,
                "provider": "aws_kms",
            }
        except ClientError as e:
            raise Exception(f"Failed to generate data key: {e}")

    def normalize_payload(self, payload: Any) -> str:
        """Normalize payload for encryption/signing."""
        if isinstance(payload, str):
            return payload
        elif isinstance(payload, dict) or isinstance(payload, list):
            return json.dumps(payload, sort_keys=True)
        else:
            return str(payload)

    def parse_encryption_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and standardize encryption result."""
        standardized = {
            "provider": "aws_kms",
            "timestamp": os.getenv("REQUEST_TIMESTAMP", ""),
            "operation": "encryption",
        }

        if "ciphertext" in result:
            standardized.update(
                {
                    "ciphertext": result["ciphertext"],
                    "key_id": result.get("key_id", ""),
                    "algorithm": result.get("encryption_algorithm", ""),
                    "type": "direct",
                }
            )
        elif "encrypted_data" in result:
            standardized.update(
                {
                    "encrypted_data": result["encrypted_data"],
                    "encrypted_dek": result.get("encrypted_dek", ""),
                    "iv": result.get("iv", ""),
                    "tag": result.get("tag", ""),
                    "key_id": result.get("key_id", ""),
                    "algorithm": result.get("encryption_mode", ""),
                    "type": "envelope",
                }
            )

        return standardized

    def parse_signature_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and standardize signature result."""
        return {
            "provider": "aws_kms",
            "signature": result.get("signature", ""),
            "key_id": result.get("key_id", ""),
            "algorithm": result.get("signing_algorithm", ""),
            "message_digest": result.get("message_digest", ""),
            "timestamp": os.getenv("REQUEST_TIMESTAMP", ""),
            "operation": "signing",
        }


# Singleton instance
_security_client_instance = None


def get_security_client() -> SecurityClient:
    """Get or create singleton security client."""
    global _security_client_instance
    if _security_client_instance is None:
        _security_client_instance = SecurityClient()
    return _security_client_instance
