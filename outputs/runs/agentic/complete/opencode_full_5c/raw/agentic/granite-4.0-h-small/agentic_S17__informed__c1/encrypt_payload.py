import os
import base64
from .security_client import kms_encrypt, kms_decrypt
from .security_models import (
    EncryptionRequest,
    EncryptionResponse,
    DecryptionRequest,
    DecryptionResponse,
)

# Encrypt Payload (Same-scenario)


def encrypt_payload(req: EncryptionRequest) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using an AWS KMS managed key.
    Returns a dict with ciphertext Blob (base64‑encoded) and encryption details.
    """
    ciphertext_blob = kms_encrypt(req["plaintext"], req["key_id"])
    # Encode blob to base64 for easy transport
    ciphertext_b64 = base64.b64encode(ciphertext_blob["CiphertextBlob"]).decode("utf-8")
    return {
        "ciphertext": ciphertext_b64,
        "key_id": ciphertext_blob["KeyId"],
        "encryption_algorithm": ciphertext_blob.get("EncryptionAlgorithm"),
    }


# Decrypt Payload (Same-scenario)


def decrypt_payload(req: DecryptionRequest) -> DecryptionResponse:
    """
    Decrypts ciphertext previously encrypted with AWS KMS.
    Returns the recovered plaintext as bytes.
    """
    plaintext = kms_decrypt(base64.b64decode(req["ciphertext"]), req["key_id"])
    return {"plaintext": plaintext}


# Envelope Encryption with AWS KMS


def envelope_encrypt(plaintext: bytes, key_id: str) -> dict:
    """
    Implements envelope encryption: generate a data key via KMS, encrypt the data with the plaintext key,
    then encrypt the data key itself with the managed key.
    Returns the ciphertext and encrypted data key for safe storage/transmission.
    """
    data_key = kms_encrypt(os.urandom(32), key_id)  # generate plaintext data key
    ciphertext = kms_encrypt(data_key["Plaintext"], key_id)["CiphertextBlob"]
    # Encrypt actual payload with the plaintext data key
    payload_enc = kms_encrypt(plaintext, data_key["KeyId"])
    return {
        "encrypted_data_key": base64.b64encode(data_key["CiphertextBlob"]).decode(
            "utf-8"
        ),
        "ciphertext": base64.b64encode(payload_enc["CiphertextBlob"]).decode("utf-8"),
    }


# Optional: simple digital signing/verification using KMS (if supported)


def sign_key(key_id: str, data: bytes) -> bytes:
    """Signs data with an AWS KMS asymmetric key (RSA/ECDSA)."""
    try:
        response = _kms.sign(KeyId=key_id, Message=data, MessageType="DIGEST")
        return response["Signature"]
    except _kms.exceptions.InvalidKeyUsageException:
        raise NotImplementedError("Signing not supported for this KMS key type")


# Optional: simple verification using KMS (if supported)


def verify_key(key_id: str, signature: bytes, data: bytes) -> bool:
    """Verifies a signature produced by sign_key. Returns bool."""
    try:
        response = _kms.verify(
            KeyId=key_id, Signature=signature, Message=data, MessageType="DIGEST"
        )
        return response["SignatureValid"]
    except _kms.exceptions.InvalidKeyUsageException:
        raise NotImplementedError("Verification not supported for this KMS key type")
