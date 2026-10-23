from azure.keyvault.keys.crypto import SignatureAlgorithm
from security_client import get_key_vault_cryptography_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse

def sign_payload(request: SignRequest):
    client = get_key_vault_cryptography_client(request.key_id)
    
    # Default to RS256 if no algorithm is specified
    algorithm = getattr(SignatureAlgorithm, request.algorithm.upper(), SignatureAlgorithm.rs256) if request.algorithm else SignatureAlgorithm.rs256

    response = client.sign(algorithm, request.digest)

    return SignResponse(
        signature=response.signature,
        key_id=request.key_id,
        algorithm=str(algorithm)
    )

def verify_payload(request: VerifyRequest):
    client = get_key_vault_cryptography_client(request.key_id)
    
    # Default to RS256 if no algorithm is specified
    algorithm = getattr(SignatureAlgorithm, request.algorithm.upper(), SignatureAlgorithm.rs256) if request.algorithm else SignatureAlgorithm.rs256

    is_valid = client.verify(algorithm, request.digest, request.signature)

    return VerifyResponse(
        is_valid=is_valid,
        key_id=request.key_id,
        algorithm=str(algorithm)
    )
