import os
import json
import base64
from typing import Dict, Any, Optional, Union
import boto3
from botocore.exceptions import ClientError


class SecurityClient:
    """Client helper for AWS KMS security operations."""

    def __init__(self, region=None, profile=None):
        self.region = region or os.environ.get("AWS_REGION", "us-east-1")
        self.profile = profile or os.environ.get("AWS_PROFILE")

        session_args = {"region_name": self.region}
        if self.profile:
            session_args["profile_name"] = self.profile

        self.session = boto3.Session(**session_args)
        self.kms_client = self.session.client("kms")

        self.encryption_key_id = os.environ.get(
            "AWS_KMS_KEY_ID", "alias/encryption-key"
        )
        self.signing_key_id = os.environ.get(
            "AWS_KMS_SIGNING_KEY_ID", "alias/signing-key"
        )

    def get_key_metadata(self, key_id=None):
        """Get metadata for a KMS key."""
        if key_id is None:
            key_id = self.encryption_key_id

        try:
            response = self.kms_client.describe_key(KeyId=key_id)
            return {
                "key_id": response["KeyMetadata"]["KeyId"],
                "arn": response["KeyMetadata"]["Arn"],
                "creation_date": response["KeyMetadata"]["CreationDate"].isoformat(),
                "description": response["KeyMetadata"].get("Description", ""),
                "key_state": response["KeyMetadata"]["KeyState"],
                "key_usage": response["KeyMetadata"]["KeyUsage"],
                "key_spec": response["KeyMetadata"]["KeySpec"],
                "origin": response["KeyMetadata"]["Origin"],
                "provider": "aws_kms",
            }
        except ClientError as e:
            raise Exception(f"Failed to get key metadata: {e}")

    def list_keys(self, limit=100):
        """List KMS keys in the region."""
        try:
            response = self.kms_client.list_keys(Limit=limit)
            keys = []
            for key in response["Keys"]:
                keys.append({"key_id": key["KeyId"], "arn": key.get("KeyArn", "")})
            return keys
        except ClientError as e:
            raise Exception(f"Failed to list keys: {e}")

    def create_alias(self, key_id, alias_name):
        """Create an alias for a KMS key."""
        try:
            self.kms_client.create_alias(
                AliasName=f"alias/{alias_name}", TargetKeyId=key_id
            )
            return {"success": True, "alias": f"alias/{alias_name}", "key_id": key_id}
        except ClientError as e:
            raise Exception(f"Failed to create alias: {e}")

    def normalize_encryption_context(self, context):
        """Normalize encryption context to AWS KMS format."""
        if context is None:
            return {}

        normalized = {}
        for key, value in context.items():
            if isinstance(value, (int, float)):
                normalized[str(key)] = str(value)
            elif isinstance(value, str):
                normalized[str(key)] = value
            else:
                normalized[str(key)] = json.dumps(value)
        return normalized

    def validate_key_id(self, key_id):
        """Validate that a key ID exists and is accessible."""
        try:
            self.kms_client.describe_key(KeyId=key_id)
            return True
        except ClientError:
            return False

    def get_client_info(self):
        """Get information about the configured client."""
        return {
            "region": self.region,
            "profile": self.profile,
            "encryption_key_id": self.encryption_key_id,
            "signing_key_id": self.signing_key_id,
            "provider": "aws_kms",
        }


def load_config_from_env():
    """Load security configuration from environment variables."""
    config = {
        "aws_region": os.environ.get("AWS_REGION", "us-east-1"),
        "aws_profile": os.environ.get("AWS_PROFILE"),
        "kms_key_id": os.environ.get("AWS_KMS_KEY_ID", "alias/encryption-key"),
        "kms_signing_key_id": os.environ.get(
            "AWS_KMS_SIGNING_KEY_ID", "alias/signing-key"
        ),
        "provider": "aws_kms",
    }

    optional_vars = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SESSION_TOKEN",
        "AWS_DEFAULT_REGION",
    ]

    for var in optional_vars:
        if var in os.environ:
            config[var.lower()] = os.environ[var]

    return config


def create_kms_client(config=None):
    """Create a KMS client from configuration."""
    if config is None:
        config = load_config_from_env()

    session_args = {"region_name": config.get("aws_region", "us-east-1")}

    if config.get("aws_profile"):
        session_args["profile_name"] = config["aws_profile"]
    elif config.get("aws_access_key_id") and config.get("aws_secret_access_key"):
        session_args["aws_access_key_id"] = config["aws_access_key_id"]
        session_args["aws_secret_access_key"] = config["aws_secret_access_key"]
        if config.get("aws_session_token"):
            session_args["aws_session_token"] = config["aws_session_token"]

    session = boto3.Session(**session_args)
    return session.client("kms")
