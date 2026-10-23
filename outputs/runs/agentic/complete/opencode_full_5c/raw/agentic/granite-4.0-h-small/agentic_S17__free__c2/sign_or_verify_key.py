# [SAME-SCENARIO] sign_or_verify_key.py

import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Provider: AWS KMS (supports signing/verification for some algorithms)
KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")


def generate_key_pair() -> tuple[bytes, bytes]:
    """Generate an RSA key pair locally (for demo only)."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ), public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def sign_with_kms(message: bytes) -> bytes:
    """Ask KMS to sign the message (if the key supports signing)."""
    # Placeholder: real implementation would call kms_client.sign(KeyId=KMS_KEY_ID, Message=message)
    # Here we sign locally with the generated private key.
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    signature = private_key.sign(
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX),
        hashes.SHA256(),
    )
    return signature


def verify_with_kms(message: bytes, signature: bytes) -> bool:
    """Verify a signature produced by KMS or locally."""
    public_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048
    ).public_key()
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False
