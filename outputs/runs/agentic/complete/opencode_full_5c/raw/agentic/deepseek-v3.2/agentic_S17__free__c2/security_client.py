import os
import json
import base64
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError


class SecurityClient:
    """Client helper utilities for Key Management and Encryption."""

    def __init__(self, region: str = None, profile: str = None):
        """
        Initialize security client with AWS configuration.

        Args:
            region: AWS region (defaults to AWS_REGION env var or 'us-east-1')
            profile: AWS profile name (defaults to default profile)
        """
        self.region = region or os.environ.get("AWS_REGION", "us-east-1")
        self.profile = profile

        # Initialize AWS clients
        session = (
            boto3.Session(profile_name=self.profile)
            if self.profile
            else boto3.Session()
        )

        self.kms_client = session.client("kms", region_name=self.region)

        # Load configuration
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load security configuration from environment and config files."""
        config = {
            "default_encryption_key": os.environ.get(
                "AWS_KMS_KEY_ID", "alias/aws/encryption-key"
            ),
            "default_signing_key": os.environ.get(
                "AWS_KMS_SIGNING_KEY_ID", "alias/aws/signing-key"
            ),
            "default_region": self.region,
            "encryption_algorithms": {
                "symmetric": "AES-GCM",
                "asymmetric": "RSA-OAEP",
                "key_wrapping": "AWS-KMS",
            },
            "signing_algorithms": [
                "RSASSA_PSS_SHA_256",
                "RSASSA_PSS_SHA_384",
                "RSASSA_PSS_SHA_512",
                "ECDSA_SHA_256",
                "ECDSA_SHA_384",
                "ECDSA_SHA_512",
            ],
        }

        # Try to load additional config from file
        config_paths = [
            "./security_config.json",
            "~/.security/config.json",
            "/etc/security/config.json",
        ]

        for path in config_paths:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                try:
                    with open(expanded_path, "r") as f:
                        file_config = json.load(f)
                        config.update(file_config)
                    break
                except (json.JSONDecodeError, IOError):
                    continue

        return config

    def get_key_metadata(self, key_id: str) -> Dict[str, Any]:
        """
        Get metadata for a KMS key.

        Args:
            key_id: AWS KMS key ID or alias

        Returns:
            Dictionary with key metadata
        """
        try:
            response = self.kms_client.describe_key(KeyId=key_id)
            metadata = response["KeyMetadata"]

            return {
                "key_id": metadata["KeyId"],
                "arn": metadata["Arn"],
                "creation_date": metadata["CreationDate"].isoformat(),
                "enabled": metadata["Enabled"],
                "description": metadata.get("Description", ""),
                "key_usage": metadata["KeyUsage"],
                "key_state": metadata["KeyState"],
                "origin": metadata["Origin"],
                "key_manager": metadata["KeyManager"],
                "customer_master_key_spec": metadata.get("CustomerMasterKeySpec", ""),
                "key_spec": metadata.get("KeySpec", ""),
                "encryption_algorithms": metadata.get("EncryptionAlgorithms", []),
                "signing_algorithms": metadata.get("SigningAlgorithms", []),
            }
        except ClientError as e:
            raise Exception(f"Failed to get key metadata: {str(e)}")

    def list_keys(self, limit: int = 100) -> list:
        """
        List available KMS keys.

        Args:
            limit: Maximum number of keys to return

        Returns:
            List of key metadata dictionaries
        """
        try:
            keys = []
            paginator = self.kms_client.get_paginator("list_keys")

            for page in paginator.paginate(Limit=limit):
                for key in page["Keys"]:
                    try:
                        key_metadata = self.get_key_metadata(key["KeyId"])
                        keys.append(key_metadata)
                    except Exception:
                        # Skip keys we can't describe
                        continue

            return keys
        except ClientError as e:
            raise Exception(f"Failed to list keys: {str(e)}")

    def rotate_key(self, key_id: str) -> Dict[str, Any]:
        """
        Rotate a KMS key (create new key material).

        Args:
            key_id: AWS KMS key ID or alias

        Returns:
            Dictionary with rotation metadata
        """
        try:
            response = self.kms_client.schedule_key_deletion(
                KeyId=key_id, PendingWindowInDays=7
            )

            # Create new key with same alias
            key_metadata = self.get_key_metadata(key_id)
            description = key_metadata.get("description", "Rotated key")

            create_response = self.kms_client.create_key(
                Description=description,
                KeyUsage=key_metadata["key_usage"],
                KeySpec=key_metadata.get(
                    "key_spec",
                    key_metadata.get("customer_master_key_spec", "SYMMETRIC_DEFAULT"),
                ),
                Origin="AWS_KMS",
            )

            new_key_id = create_response["KeyMetadata"]["KeyId"]

            # Update alias if it exists
            try:
                aliases = self.kms_client.list_aliases(KeyId=key_id)
                for alias in aliases.get("Aliases", []):
                    if alias["TargetKeyId"] == key_id:
                        alias_name = alias["AliasName"]
                        self.kms_client.update_alias(
                            AliasName=alias_name, TargetKeyId=new_key_id
                        )
                        break
            except ClientError:
                # No alias to update
                pass

            return {
                "old_key_id": key_id,
                "new_key_id": new_key_id,
                "deletion_date": response["DeletionDate"].isoformat(),
                "key_rotation": True,
                "provider": "aws_kms",
            }
        except ClientError as e:
            raise Exception(f"Failed to rotate key: {str(e)}")

    def validate_encryption_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate encryption data structure.

        Args:
            data: Encryption data dictionary

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["ciphertext", "encrypted_key", "iv", "tag"]

        for field in required_fields:
            if field not in data:
                return False

        try:
            # Try to decode base64 fields
            base64.b64decode(data["ciphertext"])
            base64.b64decode(data["encrypted_key"])
            base64.b64decode(data["iv"])
            base64.b64decode(data["tag"])

            return True
        except (KeyError, ValueError):
            return False

    def get_config(self) -> Dict[str, Any]:
        """Get current security configuration."""
        return self.config.copy()

    def update_config(self, updates: Dict[str, Any]) -> None:
        """
        Update security configuration.

        Args:
            updates: Dictionary with configuration updates
        """
        self.config.update(updates)

        # Save to environment variables where applicable
        for key, value in updates.items():
            if key.startswith("AWS_"):
                os.environ[key] = str(value)
