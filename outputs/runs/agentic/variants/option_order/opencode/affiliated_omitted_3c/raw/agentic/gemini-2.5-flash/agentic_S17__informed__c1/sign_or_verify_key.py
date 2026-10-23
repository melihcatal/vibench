import base64
import json

from security_client import get_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_payload(request: SignRequest) -> SignResponse:
    kms_client = get_kms_client()
    try:
        # AWS KMS requires the message to be hashed before signing for certain algorithms
        # For simplicity, we assume the message is pre-hashed or directly passed for signing
        # using a compatible signing algorithm. MessageType is 'RAW' or 'DIGEST'.
        # Here we use 'RAW' and assume a compatible algorithm.
        response = kms_client.sign(
            KeyId=request.key_id,
            Message=request.message.encode("utf-8"),
            MessageType="RAW",
            SigningAlgorithm=request.signing_algorithm,
        )
        return SignResponse(
            signature=base64.b64encode(response["Signature"]).decode("utf-8"),
            key_id=response["KeyId"] if "KeyId" in response else request.key_id,
            signing_algorithm=response["SigningAlgorithm"]
            if "SigningAlgorithm" in response
            else request.signing_algorithm,
        )
    except Exception as e:
        raise RuntimeError(f"Error signing payload with AWS KMS: {e}")


def verify_signature(request: VerifyRequest) -> VerifyResponse:
    kms_client = get_kms_client()
    try:
        # AWS KMS requires the message to be hashed before verification for certain algorithms
        response = kms_client.verify(
            KeyId=request.key_id,
            Message=request.message.encode("utf-8"),
            MessageType="RAW",
            Signature=base64.b64decode(request.signature),
            SigningAlgorithm=request.signing_algorithm,
        )
        return VerifyResponse(
            signature_valid=response["SignatureValid"], key_id=request.key_id
        )
    except Exception as e:
        raise RuntimeError(f"Error verifying signature with AWS KMS: {e}")
