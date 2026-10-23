import os
import base64
import boto3
from botocore.exceptions import ClientError
from security_models import SignRequest, VerifyRequest, SignResponse, VerifyResponse
from security_client import get_kms_client, validate_key_id


def sign_payload(
    message, key_id=None, message_type="RAW", signing_algorithm="RSASSA_PSS_SHA_256"
):
    request = SignRequest(
        message=message,
        key_id=key_id or os.environ.get("AWS_KMS_SIGNING_KEY_ID"),
        message_type=message_type,
        signing_algorithm=signing_algorithm,
    )
    validate_key_id(request.key_id)
    client = get_kms_client()
    try:
        message_bytes = (
            request.message.encode("utf-8")
            if isinstance(request.message, str)
            else request.message
        )
        response = client.sign(
            KeyId=request.key_id,
            Message=message_bytes,
            MessageType=request.message_type,
            SigningAlgorithm=request.signing_algorithm,
        )
        return SignResponse(
            signature=base64.b64encode(response["Signature"]).decode("utf-8"),
            key_id=response["KeyId"],
            signing_algorithm=response["SigningAlgorithm"],
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )
    except ClientError as e:
        raise RuntimeError(
            f"AWS KMS sign failed: {e.response['Error']['Message']}"
        ) from e


def verify_signature(
    message,
    signature,
    key_id=None,
    message_type="RAW",
    signing_algorithm="RSASSA_PSS_SHA_256",
):
    request = VerifyRequest(
        message=message,
        signature=signature,
        key_id=key_id or os.environ.get("AWS_KMS_SIGNING_KEY_ID"),
        message_type=message_type,
        signing_algorithm=signing_algorithm,
    )
    validate_key_id(request.key_id)
    client = get_kms_client()
    try:
        message_bytes = (
            request.message.encode("utf-8")
            if isinstance(request.message, str)
            else request.message
        )
        signature_bytes = base64.b64decode(request.signature)
        response = client.verify(
            KeyId=request.key_id,
            Message=message_bytes,
            MessageType=request.message_type,
            SigningAlgorithm=request.signing_algorithm,
            Signature=signature_bytes,
        )
        return VerifyResponse(
            signature_valid=response["SignatureValid"],
            key_id=response["KeyId"],
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )
    except ClientError as e:
        raise RuntimeError(
            f"AWS KMS verify failed: {e.response['Error']['Message']}"
        ) from e
