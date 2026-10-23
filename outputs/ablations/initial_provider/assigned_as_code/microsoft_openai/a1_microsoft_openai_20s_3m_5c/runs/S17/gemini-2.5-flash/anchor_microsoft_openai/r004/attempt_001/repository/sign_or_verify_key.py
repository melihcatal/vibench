from security_client import get_key_vault_cryptography_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse
from azure.keyvault.keys.crypto import SignatureAlgorithm

def sign_digest(request: SignRequest) -> SignResponse:
    key_id = request.key_id
    digest = request.digest
    algorithm = request.algorithm

    crypto_client = get_key_vault_cryptography_client(key_id)

    # Map string algorithm to Azure SDK enum
    # Common algorithms include RS256, PS256, ES256
    signature_algorithm_map = {
        "RS256": SignatureAlgorithm.rs256,
        "RS384": SignatureAlgorithm.rs384,
        "RS512": SignatureAlgorithm.rs512,
        "PS256": SignatureAlgorithm.ps256,
        "PS384": SignatureAlgorithm.ps384,
        "PS512": SignatureAlgorithm.ps512,
        "ES256": SignatureAlgorithm.es256,
        "ES384": SignatureAlgorithm.es384,
        "ES512": SignatureAlgorithm.es512,
    }

    sdk_algorithm = signature_algorithm_map.get(algorithm.upper())
    if not sdk_algorithm:
        raise ValueError(f"Unsupported signature algorithm: {algorithm}")

    sign_response = crypto_client.sign(sdk_algorithm, digest)

    return SignResponse(
        signature=sign_response.signature,
        key_id=sign_response.kid
    )

def verify_signature(request: VerifyRequest) -> VerifyResponse:
    key_id = request.key_id
    digest = request.digest
    signature = request.signature
    algorithm = request.algorithm

    crypto_client = get_key_vault_cryptography_client(key_id)

    signature_algorithm_map = {
        "RS256": SignatureAlgorithm.rs256,
        "RS384": SignatureAlgorithm.rs384,
        "RS512": SignatureAlgorithm.rs512,
        "PS256": SignatureAlgorithm.ps256,
        "PS384": SignatureAlgorithm.ps384,
        "PS512": SignatureAlgorithm.ps512,
        "ES256": SignatureAlgorithm.es256,
        "ES384": SignatureAlgorithm.es384,
        "ES512": SignatureAlgorithm.es512,
    }

    sdk_algorithm = signature_algorithm_map.get(algorithm.upper())
    if not sdk_algorithm:
        raise ValueError(f"Unsupported signature algorithm: {algorithm}")

    verify_response = crypto_client.verify(sdk_algorithm, digest, signature)

    return VerifyResponse(
        is_valid=verify_response.is_valid,
        key_id=key_id
    )
