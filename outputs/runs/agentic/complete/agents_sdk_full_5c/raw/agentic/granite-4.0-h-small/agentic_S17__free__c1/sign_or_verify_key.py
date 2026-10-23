from security_client import get_smc_client, get_signing_key_id

def sign_payload(payload: bytes) -> str:
    """Sign a payload using a managed asymmetric key.

    Uses AWS KMS Asymmetric signing (RSA_PSS_SHA_256). Returns a base64-encoded signature.
    """
    client = get_smc_client()  # wrapper around AWS KMS SDK
    key_id = get_signing_key_id()
    response = client.sign(KeyId=key_id,
                           Message=payload,
                           MessageType='DIGEST',
                           SigningAlgorithm='RSA_PSS_SHA_256')
    return response['Signature'].decode('utf-8')


def verify_signature(payload: bytes, signature_b64: str) -> bool:
    """Verify an existing signature against the payload using the same managed key.

    Returns True if verification succeeds, otherwise False.
    """
    client = get_smc_client()
    key_id = get_signing_key_id()
    response = client.verify(KeyId=key_id,
                             Message=payload,
                             Signature=bytes.fromhex(signature_b64),
                             MessageType='DIGEST',
                             SigningAlgorithm='RSA_PSS_SHA_256')
    return response['SignatureValid']
