# [HELPER] security_models.py

from typing import NamedTuple, Any

# Request and response data classes for same-scenario encryption/decryption tasks.
class EncryptRequest(NamedTuple):
    key_name: str  # Full resource name of the KMS CryptoKey
    plaintext: str  # UTF-8 encoded data to encrypt

    def to_protobuf(self):
        # Helper to convert to actual protobuf if needed (not used in this file).
        pass

class EncryptResponse(NamedTuple):
    ciphertext: str  # Base64‑encoded ciphertext returned by KMS

    def to_protobuf(self):
        pass

class DecryptRequest(NamedTuple):
    key_name: str  # Full resource name of the KMS CryptoKey
    ciphertext: str  # Base64‑encoded ciphertext to decrypt

    def to_protobuf(self):
        pass

class DecryptResponse(NamedTuple):
    plaintext: str  # Decrypted UTF‑8 string

class EnvelopeEncryptRequest(NamedTuple):
    plaintext: str  # Data to encrypt
    kms_key_name: str  # Full KMS CryptoKey resource name

    def to_protobuf(self):
        pass

class EnvelopeEncryptResponse(NamedTuple):
    encrypted_dek: str  # Base64‑encoded encrypted DEK (from KMS)
    encrypted_data: bytes  # DEK‑encrypted payload (local AES‑GCM)
    iv: bytes  # AES GCM IV
    auth_tag: bytes  # AES GCM authentication tag

class SignRequest(NamedTuple):
    key_name: str  # Full resource name of an asymmetric KMS CryptoKey
    data: bytes  # Raw bytes to sign

    def to_protobuf(self):
        pass

class SignResponse(NamedTuple):
    signature: str  # Base64‑encoded signature

class VerifyRequest(NamedTuple):
    key_name: str  # Full resource name of an asymmetric KMS CryptoKey
    data: bytes  # Raw bytes that were signed
    signature: bytes  # Base64‑encoded signature to verify

    def to_protobuf(self):
        pass

class VerifyResponse(NamedTuple):
    is_valid: bool  # True if the signature is valid for the data
