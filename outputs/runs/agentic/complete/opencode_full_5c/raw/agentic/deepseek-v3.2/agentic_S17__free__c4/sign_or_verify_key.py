import os
import base64
import hashlib
import json
import boto3
from botocore.exceptions import ClientError
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm


def sign_data(data, key_id=None, provider="aws"):
    """
    Sign data using a managed key service.

    Args:
        data: Data to sign (string or bytes)
        key_id: Key identifier (provider-specific)
        provider: 'aws' for AWS KMS, 'azure' for Azure Key Vault

    Returns:
        dict with signature and metadata
    """
    if not data:
        raise ValueError("Data cannot be empty")

    if isinstance(data, str):
        data_bytes = data.encode("utf-8")
    else:
        data_bytes = data

    # Hash the data
    data_hash = hashlib.sha256(data_bytes).digest()

    if provider.lower() == "aws":
        return _sign_with_aws_kms(data_hash, key_id)
    elif provider.lower() == "azure":
        return _sign_with_azure_keyvault(data_hash, key_id)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def _sign_with_aws_kms(data_hash, key_id=None):
    """Sign data using AWS KMS."""
    if not key_id:
        key_id = os.environ.get("AWS_KMS_SIGNING_KEY_ID", "alias/signing-key")

    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        response = kms_client.sign(
            KeyId=key_id,
            Message=data_hash,
            MessageType="DIGEST",
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )

        signature = response["Signature"]

        return {
            "signature": base64.b64encode(signature).decode("utf-8"),
            "algorithm": "RSASSA_PKCS1_V1_5_SHA_256",
            "key_id": key_id,
            "provider": "aws_kms",
            "message_type": "DIGEST",
        }
    except ClientError as e:
        raise Exception(f"AWS KMS signing error: {e}")


def _sign_with_azure_keyvault(data_hash, key_id=None):
    """Sign data using Azure Key Vault."""
    if not key_id:
        key_id = os.environ.get(
            "AZURE_KEY_VAULT_KEY_ID", "https://myvault.vault.azure.net/keys/mykey"
        )

    # Initialize Azure Key Vault client
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=key_id.split("/keys/")[0], credential=credential)

    key_name = key_id.split("/keys/")[1]

    try:
        # Get the key
        key = key_client.get_key(key_name)

        # Create cryptography client
        crypto_client = CryptographyClient(key, credential)

        # Sign the hash
        result = crypto_client.sign(
            algorithm=SignatureAlgorithm.rs256, digest=data_hash
        )

        return {
            "signature": base64.b64encode(result.signature).decode("utf-8"),
            "algorithm": "RS256",
            "key_id": key_id,
            "provider": "azure_keyvault",
            "key_version": key.properties.version,
        }
    except Exception as e:
        raise Exception(f"Azure Key Vault signing error: {e}")


def verify_signature(data, signature_result, provider="aws"):
    """
    Verify a signature using a managed key service.

    Args:
        data: Original data that was signed
        signature_result: dict from sign_data function
        provider: 'aws' or 'azure'

    Returns:
        bool indicating if signature is valid
    """
    if not data or not signature_result:
        raise ValueError("Data and signature result are required")

    if isinstance(data, str):
        data_bytes = data.encode("utf-8")
    else:
        data_bytes = data

    # Hash the data
    data_hash = hashlib.sha256(data_bytes).digest()

    signature = base64.b64decode(signature_result["signature"])
    key_id = signature_result.get("key_id")

    if provider.lower() == "aws":
        return _verify_with_aws_kms(
            data_hash, signature, key_id, signature_result.get("algorithm")
        )
    elif provider.lower() == "azure":
        return _verify_with_azure_keyvault(
            data_hash, signature, key_id, signature_result.get("algorithm")
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def _verify_with_aws_kms(data_hash, signature, key_id, algorithm):
    """Verify signature using AWS KMS."""
    if not key_id:
        key_id = os.environ.get("AWS_KMS_SIGNING_KEY_ID", "alias/signing-key")

    if not algorithm:
        algorithm = "RSASSA_PKCS1_V1_5_SHA_256"

    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        response = kms_client.verify(
            KeyId=key_id,
            Message=data_hash,
            MessageType="DIGEST",
            Signature=signature,
            SigningAlgorithm=algorithm,
        )

        return response["SignatureValid"]
    except ClientError as e:
        raise Exception(f"AWS KMS verification error: {e}")


def _verify_with_azure_keyvault(data_hash, signature, key_id, algorithm):
    """Verify signature using Azure Key Vault."""
    if not key_id:
        key_id = os.environ.get(
            "AZURE_KEY_VAULT_KEY_ID", "https://myvault.vault.azure.net/keys/mykey"
        )

    if not algorithm:
        algorithm = SignatureAlgorithm.rs256

    # Initialize Azure Key Vault client
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=key_id.split("/keys/")[0], credential=credential)

    key_name = key_id.split("/keys/")[1]

    try:
        # Get the key
        key = key_client.get_key(key_name)

        # Create cryptography client
        crypto_client = CryptographyClient(key, credential)

        # Verify the signature
        result = crypto_client.verify(
            algorithm=algorithm, digest=data_hash, signature=signature
        )

        return result.is_valid
    except Exception as e:
        raise Exception(f"Azure Key Vault verification error: {e}")


def create_detached_signature(data, key_id=None, provider="aws"):
    """
    Create a detached signature package.

    Args:
        data: Data to sign
        key_id: Key identifier
        provider: 'aws' or 'azure'

    Returns:
        dict with signature package
    """
    signature_result = sign_data(data, key_id, provider)

    if isinstance(data, str):
        data_encoded = base64.b64encode(data.encode("utf-8")).decode("utf-8")
    else:
        data_encoded = base64.b64encode(data).decode("utf-8")

    return {
        "data": data_encoded,
        "signature": signature_result["signature"],
        "algorithm": signature_result["algorithm"],
        "key_id": signature_result["key_id"],
        "provider": signature_result["provider"],
        "timestamp": os.environ.get("TIMESTAMP", "2024-01-01T00:00:00Z"),
    }
