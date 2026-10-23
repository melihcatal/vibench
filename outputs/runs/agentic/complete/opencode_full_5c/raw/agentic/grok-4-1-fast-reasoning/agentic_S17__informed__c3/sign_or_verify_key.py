from security_client import SecurityClient
from security_models import deserialize_bytes, serialize_bytes


def sign_message(
    message: bytes,
    key_id: str = None,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
) -> str:
    client = SecurityClient(key_id)
    response = client.kms.sign(
        KeyId=client.key_id, Message=message, SigningAlgorithm=signing_algorithm
    )
    return serialize_bytes(response["Signature"])


def verify_signature(
    message: bytes,
    signature_b64: str,
    key_id: str = None,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
) -> bool:
    client = SecurityClient(key_id)
    signature = deserialize_bytes(signature_b64)
    response = client.kms.verify(
        KeyId=client.key_id,
        Message=message,
        Signature=signature,
        SigningAlgorithm=signing_algorithm,
    )
    return response["SignatureValid"]
