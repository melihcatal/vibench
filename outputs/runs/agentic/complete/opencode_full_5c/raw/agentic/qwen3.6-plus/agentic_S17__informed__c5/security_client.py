import base64
import os
from typing import Dict, Any, Optional


def load_aws_config() -> Dict[str, str]:
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "aws_region": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    }


def load_azure_content_safety_config() -> Dict[str, str]:
    return {
        "endpoint": os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", ""),
        "api_key": os.environ.get("AZURE_CONTENT_SAFETY_KEY", ""),
    }


def load_openai_config() -> Dict[str, str]:
    return {
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    }


def load_deepl_config() -> Dict[str, str]:
    return {
        "auth_key": os.environ.get("DEEPL_AUTH_KEY", ""),
        "api_url": os.environ.get("DEEPL_API_URL", "https://api-free.deepl.com/v2"),
    }


def create_aws_kms_client():
    import boto3
    from botocore.config import Config

    config = load_aws_config()
    boto_config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
    )
    return boto3.client(
        "kms",
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        region_name=config["aws_region"],
        config=boto_config,
    )


def normalize_payload(plaintext: str) -> bytes:
    if isinstance(plaintext, str):
        return plaintext.encode("utf-8")
    return plaintext


def encode_ciphertext_blob(blob: bytes) -> str:
    return base64.b64encode(blob).decode("utf-8")


def decode_ciphertext_blob(encoded: str) -> bytes:
    return base64.b64decode(encoded.encode("utf-8"))


def normalize_encryption_context(context: Optional[Dict[str, str]]) -> Dict[str, str]:
    if context is None:
        return {}
    return {str(k): str(v) for k, v in context.items()}


def build_metadata(response_dict: Dict[str, Any]) -> Dict[str, Any]:
    metadata = {}
    http_headers = response_dict.get("ResponseMetadata", {})
    if http_headers:
        metadata["http_status_code"] = http_headers.get("HTTPStatusCode")
        metadata["request_id"] = http_headers.get("RequestId")
    return metadata


def handle_kms_error(exc: Exception, operation: str) -> Exception:
    error_msg = f"KMS {operation} failed: {str(exc)}"
    return RuntimeError(error_msg)


def validate_key_id(key_id: str) -> None:
    if not key_id or not key_id.strip():
        raise ValueError("key_id cannot be empty")


def validate_plaintext(plaintext: str) -> None:
    if not plaintext:
        raise ValueError("plaintext cannot be empty")


def validate_ciphertext(ciphertext: str) -> None:
    if not ciphertext:
        raise ValueError("ciphertext cannot be empty")
