from azure.keyvault.keys.crypto import SignatureAlgorithm
from security_client import get_cryptography_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse

def sign_payload(request: SignRequest) -> SignResponse:
    client = get_cryptography_client(request.key_id)
    
    # Map string algorithm to Enum if necessary. Assuming RSA-PSS or ECDSA for signing.
    # For this example, let's assume RS256 as a common signing algorithm.
    # The digest needs to be pre-hashed before sending to Key Vault.
    if request.algorithm.upper() == "RS256":
        akv_algorithm = SignatureAlgorithm.rs256
    elif request.algorithm.upper() == "RS384":
        akv_algorithm = SignatureAlgorithm.rs384
    elif request.algorithm.upper() == "RS512":
        akv_algorithm = SignatureAlgorithm.rs512
    else:
        raise ValueError(f"Unsupported signing algorithm: {request.algorithm}")

    sign_result = client.sign(akv_algorithm, request.digest)
    return SignResponse(
        signature=sign_result.signature,
        key_id=request.key_id,
        algorithm=request.algorithm
    )

def verify_payload(request: VerifyRequest) -> VerifyResponse:
    client = get_cryptography_client(request.key_id)

    if request.algorithm.upper() == "RS256":
        akv_algorithm = SignatureAlgorithm.rs256
    elif request.algorithm.upper() == "RS384":
        akv_algorithm = SignatureAlgorithm.rs384
    elif request.algorithm.upper() == "RS512":
        akv_algorithm = SignatureAlgorithm.rs512
    else:
        raise ValueError(f"Unsupported verification algorithm: {request.algorithm}")

    verify_result = client.verify(
        akv_algorithm,
        request.digest,
        request.signature
    )
    return VerifyResponse(
        is_valid=verify_result.is_valid,
        key_id=request.key_id,
        algorithm=request.algorithm
    )
