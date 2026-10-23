import json
from security_client import get_key_management_client

# AWS KMS signing/verification example (if algorithm supports)

def sign_data(data: str, key_id: str) -> str:
    """Sign arbitrary data using the RSA key's private key.

    Returns the base64‑encoded signature.
    """
    client = get_key_management_client()
    response = client.sign(KeyId=key_id, Message=data.encode('utf-8'),
                           SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256')
    return base64.b64encode(response['Signature']).decode('utf-8')


def verify_signature(data: str, signature_b64: str, key_id: str) -> bool:
    """Verify a signature produced by sign_data.",
    client = get_key_management_client()
    signature = base64.b64decode(signature_b64)
    response = client.verify(KeyId=key_id, Message=data.encode('utf-8'),
                             Signature=signature, SigningAlgorithm=
                             'RSASSA_PKCS1_V1_5_SHA_256')
    return response['SignatureValid']
