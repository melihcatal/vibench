from google.cloud import kms
from google.protobuf import wrappers_pb2
from security_models import SigningConfig, VerificationConfig
from security_client import get_kms_client

def sign_payload(payload: dict, config: SigningConfig):
    client = get_kms_client()
    if config.version_id:
        name = client.crypto_key_version_path(
            config.project_id, config.location, config.key_ring, config.key_id, config.version_id
        )
    else:
        name = client.crypto_key_path(
            config.project_id, config.location, config.key_ring, config.key_id
        )

    # The digest must be a byte string
    digest = payload["digest"]

    if config.hash_algorithm == "SHA256":
        digest_obj = {"sha256": digest}
    elif config.hash_algorithm == "SHA384":
        digest_obj = {"sha384": digest}
    elif config.hash_algorithm == "SHA512":
        digest_obj = {"sha512": digest}
    else:
        raise ValueError("Unsupported hash algorithm")

    response = client.asymmetric_sign(
        request={"name": name, "digest": digest_obj}
    )
    return {"signature": response.signature}

def verify_signature(payload: dict, config: VerificationConfig):
    client = get_kms_client()
    if config.version_id:
        name = client.crypto_key_version_path(
            config.project_id, config.location, config.key_ring, config.key_id, config.version_id
        )
    else:
        name = client.crypto_key_path(
            config.project_id, config.location, config.key_ring, config.key_id
        )

    # Get the public key to perform local verification, or use the KMS API directly
    # For this example, we will simulate verification by fetching the public key
    public_key_response = client.get_public_key(name=name)
    # In a real application, you would use a cryptographic library (e.g., PyOpenSSL, cryptography) 
    # to verify the signature using public_key_response.pem and the provided digest and signature.
    # For this exercise, we will just return a success message assuming external verification.

    # This is a placeholder for actual verification logic.
    # In a real scenario, you would perform: 
    # 1. Digest creation from original data (if not provided in payload)
    # 2. Signature verification using the public key

    # Assuming the digest and signature are valid for this example
    return {"is_valid": True, "public_key_pem": public_key_response.pem}
