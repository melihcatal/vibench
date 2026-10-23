from security_client import SecurityClient
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse
import base64
from hashlib import sha256


def sign_message(request: SignRequest) -> SignResponse:
    client = SecurityClient()
    # Hash the message before signing
    message_hash = sha256(request.message.encode("utf-8")).digest()
    response = client.kms_client.sign(
        KeyId=request.key_id,
        Message=message_hash,
        MessageType="DIGEST",
        SigningAlgorithm="ECDSA_SHA_256",  # Or RSASSA_PSS_SHA_256, etc.
    )
    return SignResponse(key_id=request.key_id, signature=response["Signature"])


def verify_signature(request: VerifyRequest) -> VerifyResponse:
    client = SecurityClient()
    message_hash = sha256(request.message.encode("utf-8")).digest()
    signature_blob = base64.b64decode(request.signature)
    response = client.kms_client.verify(
        KeyId=request.key_id,
        Message=message_hash,
        MessageType="DIGEST",
        Signature=signature_blob,
        SigningAlgorithm="ECDSA_SHA_256",  # Must match the signing algorithm
    )
    return VerifyResponse(
        key_id=request.key_id, signature_valid=response["SignatureValid"]
    )
