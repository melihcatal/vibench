from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import SignRequest, SignResponse
import base64
import hashlib


def sign_message(request: SignRequest) -> SignResponse:
    client = get_kms_client()
    key_name = (
        request.key_name
    )  # projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*
    message_bytes = request.message.encode("utf-8")

    # KMS requires the message to be hashed before signing for asymmetric keys.
    # For SHA256, we calculate the digest locally.
    digest = hashlib.sha256(message_bytes).digest()

    response = client.asymmetric_sign(
        request={"name": key_name, "digest": {"sha256": digest}}
    )
    return SignResponse(signature=response.signature, key_name=key_name)


def get_public_key_for_verification(key_name: str) -> str:
    client = get_kms_client()
    # key_name should be projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*
    public_key_response = client.get_public_key(name=key_name)
    return public_key_response.pem
