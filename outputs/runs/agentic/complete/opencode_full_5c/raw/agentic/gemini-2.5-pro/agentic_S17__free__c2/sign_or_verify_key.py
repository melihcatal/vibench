import hashlib
from azure.keyvault.keys.crypto import SignatureAlgorithm
from security_client import get_azure_crypto_client
from security_models import SigningPayload, VerificationPayload


def sign_message(payload: SigningPayload) -> bytes:
    crypto_client = get_azure_crypto_client(payload.key_id)

    digest = hashlib.sha256(payload.data_to_sign).digest()

    sign_result = crypto_client.sign(SignatureAlgorithm.RS256, digest)
    return sign_result.signature


def verify_signature(payload: VerificationPayload) -> bool:
    crypto_client = get_azure_crypto_client(payload.key_id)

    digest = hashlib.sha256(payload.original_data).digest()

    verify_result = crypto_client.verify(
        SignatureAlgorithm.RS256, digest, payload.signature
    )
    return verify_result.is_valid
