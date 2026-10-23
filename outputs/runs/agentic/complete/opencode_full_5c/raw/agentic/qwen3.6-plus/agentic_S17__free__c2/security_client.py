import os
import json
import base64
from typing import Optional, Dict, Any

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import (
    EncryptRequest,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    normalize_plaintext,
    normalize_ciphertext,
    format_ciphertext_for_storage,
)


def load_kms_config() -> Dict[str, Any]:
    region = os.environ.get(
        "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
    )
    endpoint_url = os.environ.get("AWS_KMS_ENDPOINT_URL")
    config_kwargs = {
        "region_name": region,
        "retries": {
            "max_attempts": int(os.environ.get("AWS_RETRY_MAX_ATTEMPTS", "3")),
            "mode": os.environ.get("AWS_RETRY_MODE", "standard"),
        },
    }
    if endpoint_url:
        config_kwargs["endpoint_url"] = endpoint_url
    return config_kwargs


def get_kms_client(config: Optional[Dict[str, Any]] = None):
    if config is None:
        config = load_kms_config()
    boto_config = Config(
        retries=config.get("retries", {"max_attempts": 3, "mode": "standard"})
    )
    client_kwargs = {
        "service_name": "kms",
        "config": boto_config,
    }
    if config.get("region_name"):
        client_kwargs["region_name"] = config["region_name"]
    if config.get("endpoint_url"):
        client_kwargs["endpoint_url"] = config["endpoint_url"]
    return boto3.client(**client_kwargs)


def execute_encrypt(request: EncryptRequest, client=None) -> EncryptResponse:
    if client is None:
        client = get_kms_client()
    plaintext = normalize_plaintext(request.plaintext)
    kwargs: Dict[str, Any] = {
        "KeyId": request.key_id,
        "Plaintext": plaintext,
        "EncryptionAlgorithm": request.encryption_algorithm.value,
    }
    if request.encryption_context:
        kwargs["EncryptionContext"] = request.encryption_context
    if request.grant_tokens:
        kwargs["GrantTokens"] = request.grant_tokens
    response = client.encrypt(**kwargs)
    return EncryptResponse(
        ciphertext_blob=response["CiphertextBlob"],
        key_id=response["KeyId"],
        encryption_algorithm=response["EncryptionAlgorithm"],
        request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        http_status_code=response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0),
    )


def execute_decrypt(request: DecryptRequest, client=None) -> DecryptResponse:
    if client is None:
        client = get_kms_client()
    ciphertext = normalize_ciphertext(request.ciphertext_blob)
    kwargs: Dict[str, Any] = {
        "CiphertextBlob": ciphertext,
        "EncryptionAlgorithm": request.encryption_algorithm.value,
    }
    if request.encryption_context:
        kwargs["EncryptionContext"] = request.encryption_context
    if request.grant_tokens:
        kwargs["GrantTokens"] = request.grant_tokens
    response = client.decrypt(**kwargs)
    return DecryptResponse(
        plaintext=response["Plaintext"],
        key_id=response["KeyId"],
        encryption_algorithm=response["EncryptionAlgorithm"],
        request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        http_status_code=response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0),
    )


def execute_envelope_encrypt(
    request: EnvelopeEncryptRequest, client=None
) -> EnvelopeEncryptResponse:
    if client is None:
        client = get_kms_client()
    gdk_kwargs: Dict[str, Any] = {
        "KeyId": request.key_id,
        "NumberOfBytes": request.number_of_bytes,
    }
    if request.encryption_context:
        gdk_kwargs["EncryptionContext"] = request.encryption_context
    gdk_response = client.generate_data_key(**gdk_kwargs)
    data_key = gdk_response["Plaintext"]
    encrypted_data_key = gdk_response["CiphertextBlob"]
    data_key_id = gdk_response["KeyId"]
    enc_request = EncryptRequest(
        key_id=data_key_id,
        plaintext=request.plaintext,
        encryption_context=request.encryption_context,
        encryption_algorithm=request.encryption_algorithm,
    )
    enc_response = execute_encrypt(enc_request, client=client)
    return EnvelopeEncryptResponse(
        encrypted_data_key=encrypted_data_key,
        ciphertext_blob=enc_response.ciphertext_blob,
        key_id=data_key_id,
        encryption_context=request.encryption_context or {},
        request_id=enc_response.request_id,
        http_status_code=enc_response.http_status_code,
    )


def execute_sign(request: SignRequest, client=None) -> SignResponse:
    if client is None:
        client = get_kms_client()
    message = normalize_plaintext(request.message)
    kwargs: Dict[str, Any] = {
        "KeyId": request.key_id,
        "Message": message,
        "SigningAlgorithm": request.signing_algorithm.value,
        "MessageType": request.message_type.value,
    }
    if request.encryption_context:
        kwargs["EncryptionContext"] = request.encryption_context
    if request.grant_tokens:
        kwargs["GrantTokens"] = request.grant_tokens
    response = client.sign(**kwargs)
    return SignResponse(
        signature=response["Signature"],
        key_id=response["KeyId"],
        signing_algorithm=response["SigningAlgorithm"],
        request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        http_status_code=response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0),
    )


def execute_verify(request: VerifyRequest, client=None) -> VerifyResponse:
    if client is None:
        client = get_kms_client()
    message = normalize_plaintext(request.message)
    signature = normalize_ciphertext(request.signature)
    kwargs: Dict[str, Any] = {
        "KeyId": request.key_id,
        "Message": message,
        "Signature": signature,
        "SigningAlgorithm": request.signing_algorithm.value,
        "MessageType": request.message_type.value,
    }
    if request.encryption_context:
        kwargs["EncryptionContext"] = request.encryption_context
    if request.grant_tokens:
        kwargs["GrantTokens"] = request.grant_tokens
    response = client.verify(**kwargs)
    return VerifyResponse(
        signature_valid=response["SignatureValid"],
        key_id=response["KeyId"],
        signing_algorithm=response["SigningAlgorithm"],
        request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        http_status_code=response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0),
    )


def get_key_metadata(key_id: str, client=None) -> Dict[str, Any]:
    if client is None:
        client = get_kms_client()
    response = client.describe_key(KeyId=key_id)
    return response["KeyMetadata"]


def list_key_usage_events(key_id: str, max_results: int = 50, client=None) -> list:
    if client is None:
        client = get_kms_client()
    events = []
    paginator = client.get_paginator("list_keys")
    for page in paginator.paginate():
        for key in page["Keys"]:
            if key["KeyId"] == key_id or key["KeyId"].endswith(key_id):
                events.append(key)
    return events[:max_results]


def serialize_response_for_api(response_obj) -> Dict[str, Any]:
    result = {}
    for field_name, value in response_obj.__dict__.items():
        if isinstance(value, bytes):
            result[field_name] = format_ciphertext_for_storage(value)
        elif hasattr(value, "value"):
            result[field_name] = value.value
        elif isinstance(value, dict):
            result[field_name] = value
        else:
            result[field_name] = value
    return result
