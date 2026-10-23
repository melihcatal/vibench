from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse

def sign_digest(request: SignRequest, config=None) -> SignResponse:
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(request.key_id, credential=credential) as client:
            # For RSA keys, the digest needs to be hashed first by the caller.
            # Assuming the digest provided is already hashed with SHA256 or similar.
            # The algorithm should be chosen based on the key type in Key Vault.
            # For example, RS256 for RSA keys, ES256 for EC keys.
            # Here, we'll use RS256 as a common example.
            signature_algorithm = SignatureAlgorithm.rs256
            response = client.sign(signature_algorithm, request.digest)
    return SignResponse(signature=response.signature, key_id=response.key_id, algorithm=signature_algorithm.value)

def verify_signature(request: VerifyRequest, config=None) -> VerifyResponse:
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(request.key_id, credential=credential) as client:
            # The algorithm used for signing must match the one used for verification.
            # Assuming the request.algorithm is a valid SignatureAlgorithm string.
            signature_algorithm = SignatureAlgorithm(request.algorithm)
            is_valid = client.verify(signature_algorithm, request.digest, request.signature)
    return VerifyResponse(is_valid=is_valid)
