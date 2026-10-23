from security_client import KmsClient
from security_models import (
    SignatureRequest,
    SignatureResponse,
    VerificationRequest,
    VerificationResponse,
)
import hashlib


def sign_payload(request: SignatureRequest) -> SignatureResponse:
    kms_client = KmsClient().get_client()

    # AWS KMS signing operations require the message to be hashed first
    # The digest algorithm must match the signing algorithm specified.
    # For simplicity, we'll use SHA256 for the message digest here.
    message_digest = hashlib.sha256(request.message).digest()

    response = kms_client.sign(
        KeyId=request.key_id,
        Message=message_digest,
        MessageType="DIGEST",
        SigningAlgorithm=request.signing_algorithm,
    )

    return SignatureResponse(
        signature=response["Signature"],
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm,
    )


def verify_signature(request: VerificationRequest) -> VerificationResponse:
    kms_client = KmsClient().get_client()

    # AWS KMS verification operations require the message to be hashed first
    message_digest = hashlib.sha256(request.message).digest()

    response = kms_client.verify(
        KeyId=request.key_id,
        Message=message_digest,
        MessageType="DIGEST",
        Signature=request.signature,
        SigningAlgorithm=request.signing_algorithm,
    )

    return VerificationResponse(
        is_valid=response["SignatureValid"],
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm,
    )
