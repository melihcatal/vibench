import os
import base64
import hashlib
import boto3
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse
from security_client import get_kms_client, load_aws_config


def sign_data(
    data: str, key_id: str = None, signing_algorithm: str = "RSASSA_PSS_SHA_256"
) -> SignResponse:
    config = load_aws_config()
    kms_client = get_kms_client(config)

    request = SignRequest(
        key_id=key_id or os.environ.get("AWS_KMS_SIGNING_KEY_ID"),
        message=data.encode("utf-8"),
        signing_algorithm=signing_algorithm,
    )

    message_hash = hashlib.sha256(request.message).digest()

    params = {
        "KeyId": request.key_id,
        "Message": message_hash,
        "MessageType": "DIGEST",
        "SigningAlgorithm": request.signing_algorithm,
    }

    response = kms_client.sign(**params)

    signature_b64 = base64.b64encode(response["Signature"]).decode("utf-8")

    return SignResponse(
        signature=signature_b64,
        key_id=response["KeyId"],
        signing_algorithm=response["SigningAlgorithm"],
        request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
    )


def verify_signature(
    data: str,
    signature_b64: str,
    key_id: str = None,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
) -> VerifyResponse:
    config = load_aws_config()
    kms_client = get_kms_client(config)

    request = VerifyRequest(
        key_id=key_id or os.environ.get("AWS_KMS_SIGNING_KEY_ID"),
        message=data.encode("utf-8"),
        signature=base64.b64decode(signature_b64),
        signing_algorithm=signing_algorithm,
    )

    message_hash = hashlib.sha256(request.message).digest()

    params = {
        "KeyId": request.key_id,
        "Message": message_hash,
        "MessageType": "DIGEST",
        "Signature": request.signature,
        "SigningAlgorithm": request.signing_algorithm,
    }

    response = kms_client.verify(**params)

    return VerifyResponse(
        signature_valid=response["SignatureValid"],
        key_id=response["KeyId"],
        signing_algorithm=response["SigningAlgorithm"],
        request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
    )


if __name__ == "__main__":
    sign_result = sign_data("Data to sign")
    print(sign_result.signature[:50])
