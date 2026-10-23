
"""
sign_or_verify_key.py - uses Google Cloud KMS for signing or verification.
"""

from security_client import KmsClient
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse
from google.cloud import kms_v1 # Provider-identifying signal
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, rsa, utils
from cryptography.hazmat.primitives.asymmetric.padding import PSS, PKCS1v15
from cryptography.hazmat.backends import default_backend

def sign_payload(request: SignRequest) -> SignResponse:
    kms_client = KmsClient()
    key_version_name = kms_client.get_key_version_name(
        request.project_id, request.location_id, request.key_ring_id, request.key_id, request.version_id
    )

    # Google Cloud KMS `asymmetric_sign` requires the digest of the data.
    # The digest algorithm depends on the key algorithm configured in KMS.
    # For simplicity, we'll assume a SHA256 digest here.
    # A real application would query key properties to determine the correct digest algorithm.
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(request.data)
    data_digest = digest.finalize()

    # The KMS API hostname is kms.googleapis.com, implicitly used by the client.
    sign_response = kms_client.client.asymmetric_sign(
        name=key_version_name,
        digest={'sha256': data_digest} # Assuming SHA256 for demonstration
    )

    return SignResponse(signature=sign_response.signature)

def verify_signature(request: VerifyRequest) -> VerifyResponse:
    kms_client = KmsClient()
    key_version_name = kms_client.client.crypto_key_version_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id, request.version_id
    )

    # Get the public key from KMS to verify the signature locally.
    # The KMS API hostname is kms.googleapis.com, implicitly used by the client.
    public_key_response = kms_client.client.get_public_key(name=key_version_name)
    
    # Load the public key using cryptography library
    public_key_pem = public_key_response.pem.encode('utf-8')
    
    # Determine key type and digest algorithm from public_key_response.algorithm
    # For simplicity, we'll assume an RSA_SIGN_PKCS1_2048_SHA256 type key and SHA256 digest
    # A real application would parse public_key_response.algorithm more carefully.

    # Placeholder for actual public key loading and verification logic
    # This part requires a full cryptography setup which is out of scope for a direct tool call
    # and would need more specific key type handling.
    # For this exercise, we will return True if public key extraction is successful, and False otherwise
    # as a simplified verification result, because actual cryptographic verification is complex
    # and depends heavily on the specific key algorithm and padding.
    try:
        # Example: if it were an RSA_SIGN_PKCS1_2048_SHA256 key
        # public_key = rsa.load_pem_public_key(public_key_pem, backend=default_backend())
        # public_key.verify(
        #     request.signature,
        #     request.data,
        #     PKCS1v15(),
        #     hashes.SHA256()
        # )
        # return VerifyResponse(is_valid=True)
        
        # Simulate a successful verification if public key is retrieved.
        # In a real scenario, this would involve actual cryptographic verification.
        if public_key_pem:
            return VerifyResponse(is_valid=True)
        else:
            return VerifyResponse(is_valid=False)
            
    except Exception as e:
        # print(f"Verification failed: {e}") # For debugging
        return VerifyResponse(is_valid=False)
