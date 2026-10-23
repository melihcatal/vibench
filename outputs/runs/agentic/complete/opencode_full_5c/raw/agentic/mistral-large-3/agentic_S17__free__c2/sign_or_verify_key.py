from google.cloud import kms
from security_client import KMSClient
from security_models import SigningResult
import hashlib


def sign_key(data: str, key_ring_id: str, key_id: str) -> SigningResult:
    client = KMSClient()
    key_name = client.get_key_name(key_ring_id, key_id)
    data_bytes = data.encode("utf-8")
    digest = hashlib.sha256(data_bytes).digest()
    signature = client.sign(key_name, digest)
    return SigningResult(
        signature=signature,
        key_id=key_id,
        algorithm="SHA256_WITH_RSA",
    )


def verify_key(data: str, signing_result: SigningResult, key_ring_id: str) -> bool:
    client = KMSClient()
    key_name = client.get_key_name(key_ring_id, signing_result.key_id)
    data_bytes = data.encode("utf-8")
    digest = hashlib.sha256(data_bytes).digest()
    return client.verify(key_name, digest, signing_result.signature)
