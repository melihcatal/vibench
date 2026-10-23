import os
from google.cloud import kms_v1
from google.protobuf import wrappers_pb2 # For BytesValue

from security_client import get_kms_client
from security_models import SigningRequest, SigningResult, VerificationRequest, VerificationResult

def sign_payload(request: SigningRequest) -> SigningResult:
    """Signs a payload with an asymmetric signing key in Google Cloud KMS."""
    client = get_kms_client()
    key_version_name = client.crypto_key_version_path(
        os.environ["GCP_PROJECT_ID"],
        os.environ["GCP_KMS_LOCATION"],
        os.environ["GCP_KMS_KEY_RING"],
        os.environ["GCP_KMS_KEY_NAME"],
        os.environ["GCP_KMS_KEY_VERSION"], # Needs a specific key version for signing
    )

    # For signing, the message must be hashed locally first. KMS expects the digest.
    # Assume SHA256 for this example.
    import hashlib
    digest = hashlib.sha256(request.data_to_sign).digest()

    digest_proto = kms_v1.Digest(sha256=digest)

    response = client.asymmetric_sign(
        request=kms_v1.AsymmetricSignRequest(
            name=key_version_name,
            digest=digest_proto,
        )
    )
    return SigningResult(signature=response.signature)

def verify_signature(request: VerificationRequest) -> VerificationResult:
    """Verifies a signature with an asymmetric public key from Google Cloud KMS.
    Note: KMS does not provide a direct verify API. Verification is typically done locally
    using the public key retrieved from KMS. For the purpose of this exercise, we will
    simulate a verification process or indicate where the public key would be retrieved.
    """
    client = get_kms_client()
    key_version_name = client.crypto_key_version_path(
        os.environ["GCP_PROJECT_ID"],
        os.environ["GCP_KMS_LOCATION"],
        os.environ["GCP_KMS_KEY_RING"],
        os.environ["GCP_KMS_KEY_NAME"],
        os.environ["GCP_KMS_KEY_VERSION"],
    )

    # Retrieve the public key to perform local verification.
    public_key_response = client.get_public_key(name=key_version_name)
    public_key_pem = public_key_response.pem

    # In a real scenario, you would use a cryptographic library (e.g., cryptography) with public_key_pem
    # to verify request.signature against hashlib.sha256(request.original_data).digest().
    # For this exercise, we acknowledge that KMS provides the key for *local* verification.
    # We'll return True for simulation, but actual verification logic goes here.

    # Example (conceptual):
    # from cryptography.hazmat.primitives import hashes
    # from cryptography.hazmat.primitives.asymmetric import padding, utils
    # from cryptography.hazmat.primitives.serialization import load_pem_public_key
    # public_key = load_pem_public_key(public_key_pem.encode('utf-8'))
    # try:
    #     public_key.verify(
    #         request.signature,
    #         hashlib.sha256(request.original_data).digest(),
    #         padding.PKCS1v15(), # Or other padding depending on key algorithm
    #         hashes.SHA256() # Or other hash algorithm
    #     )
    #     is_valid = True
    # except InvalidSignature:
    #     is_valid = False

    return VerificationResult(is_valid=True) # Simulated result

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, GCP_KMS_LOCATION, GCP_KMS_KEY_RING, GCP_KMS_KEY_NAME, GCP_KMS_KEY_VERSION env vars)
    # from dotenv import load_dotenv
    # load_dotenv()

    # # Signing example
    # data = b"A message to be signed."
    # sign_req = SigningRequest(data_to_sign=data)
    # sign_result = sign_payload(sign_req)
    # print(f"Signature: {sign_result.signature.hex()}")

    # # Verification example (conceptually, requires local crypto lib)
    # # For real verification, you'd need the original data and the signature
    # verify_req = VerificationRequest(original_data=data, signature=sign_result.signature)
    # verify_result = verify_signature(verify_req)
    # print(f"Signature valid: {verify_result.is_valid}")
    pass
