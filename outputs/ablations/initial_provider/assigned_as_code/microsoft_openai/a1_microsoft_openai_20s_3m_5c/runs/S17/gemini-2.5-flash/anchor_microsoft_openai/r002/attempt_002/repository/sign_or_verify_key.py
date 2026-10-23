from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm
from security_client import get_key_vault_crypto_client
from security_models import SignaturePayload, VerificationPayload, SignedResult, VerifiedResult
import base64

def sign_payload(payload: SignaturePayload, config=None) -> SignedResult:
    config = config or {}
    key_id = config['key_id']

    # The algorithm should be one supported by Azure Key Vault for signing, e.g., PS256, RS256.
    # We'll map the string algorithm to the SignatureAlgorithm enum.
    signature_algorithm_map = {
        "PS256": SignatureAlgorithm.ps256,
        "PS384": SignatureAlgorithm.ps384,
        "PS512": SignatureAlgorithm.ps512,
        "RS256": SignatureAlgorithm.rs256,
        "RS384": SignatureAlgorithm.rs384,
        "RS512": SignatureAlgorithm.rs512,
        "ES256": SignatureAlgorithm.es256,
        "ES384": SignatureAlgorithm.es384,
        "ES512": SignatureAlgorithm.es512,
        "ES256K": SignatureAlgorithm.es256k,
    }
    
    # Ensure the algorithm is provided and is valid
    if payload.algorithm not in signature_algorithm_map:
        raise ValueError(f"Unsupported signature algorithm: {payload.algorithm}")

    signature_algorithm = signature_algorithm_map[payload.algorithm]

    with get_key_vault_crypto_client(key_id) as client:
        sign_response = client.sign(signature_algorithm, payload.digest)
    
    return SignedResult(signature=sign_response.signature, key_id=key_id)


def verify_payload(payload: VerificationPayload, config=None) -> VerifiedResult:
    config = config or {}
    key_id = config['key_id']

    signature_algorithm_map = {
        "PS256": SignatureAlgorithm.ps256,
        "PS384": SignatureAlgorithm.ps384,
        "PS512": SignatureAlgorithm.ps512,
        "RS256": SignatureAlgorithm.rs256,
        "RS384": SignatureAlgorithm.rs384,
        "RS512": SignatureAlgorithm.rs512,
        "ES256": SignatureAlgorithm.es256,
        "ES384": SignatureAlgorithm.es384,
        "ES512": SignatureAlgorithm.es512,
        "ES256K": SignatureAlgorithm.es256k,
    }

    if payload.algorithm not in signature_algorithm_map:
        raise ValueError(f"Unsupported signature algorithm: {payload.algorithm}")

    signature_algorithm = signature_algorithm_map[payload.algorithm]

    with get_key_vault_crypto_client(key_id) as client:
        verify_response = client.verify(signature_algorithm, payload.digest, payload.signature)
    
    return VerifiedResult(is_valid=verify_response.is_valid, key_id=key_id)
