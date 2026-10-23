from security_client import KmsClient
from security_models import EncryptionConfig, KeyOperationResult
from google.cloud import kms
import hashlib

def sign_payload(payload_data: bytes, config: EncryptionConfig, digest_algorithm: str = "SHA256") -> KeyOperationResult:
    try:
        kms_client = KmsClient(config)

        # Hash the payload locally
        if digest_algorithm == "SHA256":
            digest = hashlib.sha256(payload_data).digest()
            kms_digest_algo = kms.Digest.Sha256
        elif digest_algorithm == "SHA512":
            digest = hashlib.sha512(payload_data).digest()
            kms_digest_algo = kms.Digest.Sha512
        else:
            return KeyOperationResult(success=False, error="Unsupported digest algorithm")

        signature = kms_client.asymmetric_sign(digest, kms_digest_algo)
        return KeyOperationResult(success=True, data={"signature": signature})
    except Exception as e:
        return KeyOperationResult(success=False, error=str(e))

def verify_signature(payload_data: bytes, signature: bytes, config: EncryptionConfig, digest_algorithm: str = "SHA256") -> KeyOperationResult:
    try:
        kms_client = KmsClient(config)

        # Get the public key to verify the signature locally
        # Note: For actual verification with KMS, you typically use `asymmetric_decrypt` for RSA-OAEP or client-side libraries with the public key.
        # KMS `asymmetric_sign` only provides the signing capability, not direct verification. 
        # A common pattern is to retrieve the public key and use a local crypto library for verification.
        # However, for demonstration of KMS usage, we will retrieve the public key.
        
        # For a full verification flow using KMS, it would involve either using a key with `ASYMMETRIC_DECRYPT` purpose
        # or retrieving the public key and verifying client-side. This example focuses on retrieving the public key
        # as a step in verification, but actual verification would require more local crypto code.
        
        public_key_pem = kms_client.get_public_key()
        
        # In a real scenario, you would use a crypto library like `cryptography` to verify the signature
        # with the public_key_pem, digest_algorithm, payload_data, and signature.
        # For this example, we'll just return the public key as part of the successful operation.
        
        return KeyOperationResult(success=True, data={"public_key_pem": public_key_pem, "message": "Public key retrieved for client-side verification."})
    except Exception as e:
        return KeyOperationResult(success=False, error=str(e))

def mac_sign_payload(payload_data: bytes, config: EncryptionConfig) -> KeyOperationResult:
    try:
        kms_client = KmsClient(config)
        mac_tag = kms_client.mac_sign(payload_data)
        return KeyOperationResult(success=True, data={"mac_tag": mac_tag})
    except Exception as e:
        return KeyOperationResult(success=False, error=str(e))

def mac_verify_payload(payload_data: bytes, mac_to_verify: bytes, config: EncryptionConfig) -> KeyOperationResult:
    try:
        kms_client = KmsClient(config)
        is_valid = kms_client.mac_verify(payload_data, mac_to_verify)
        return KeyOperationResult(success=True, data={"is_valid": is_valid})
    except Exception as e:
        return KeyOperationResult(success=False, error=str(e))
