# sign_or_verify_key.py
import os
from security_client import SecurityClient, SecurityModels

# AWS KMS (same-scenario) - signing and verification

def create_sign_associated_key_pair(key_spec: str = "RSA_2048") -> str:
    """Create an asymmetric CMK for signing/verification and return its key ID."""
    client = SecurityClient()
    response = client._kms.create_key(
        Description="Key for signing/verification",
        KeyUsage="SIGN_VERIFY",
        KeySpec=key_spec,
        KeyPolicy="{
          \"Version\": \"2012-10-17\",
          \"Statement\": [
            {
              \"Effect\": \"Allow\",
              \"Principal\": {\"AWS\": \"*\"},
              \"Action\": [\"kms:Sign\", \"kms:Verify\"],
              \"Resource\": \"*\"
            }
          ]
        }"
    )
    return response["KeyMetadata"]["KeyId"]


def sign_message(key_id: str, message: bytes, algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256") -> bytes:
    """Sign a message using the specified asymmetric KMS key."""
    client = SecurityClient()
    resp = client.sign(key_id=key_id, message=message, signing_algorithm=algorithm)
    return resp["Signature"]


def verify_signature(key_id: str, message: bytes, signature: bytes,
                     algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256") -> bool:
    """Verify a signature using the specified asymmetric KMS key."""
    client = SecurityClient()
    resp = client.verify(KeyId=key_id, Message=message, Signature=signature,
                         SigningAlgorithm=algorithm, MessageType="RAW")
    return resp["SigningResult"] == "SUCCESS"


def associate_key_for_verification(key_id: str) -> bool:
    """Check that the key allows verification (useful for compliance checks)."""
    client = SecurityClient()
    policy = client._kms.get_key_policy(KeyId=key_id, PolicyName="default")
    # Simplified check for demonstration
    return "kms:Verify" in policy["Policy"]
