from security_client import KMSClient
from security_models import serialize_payload, normalize_base64, denormalize_base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


def envelope_encrypt(plaintext: str) -> dict:
    client = KMSClient()
    plaintext_bytes = serialize_payload(plaintext)

    # Generate a data encryption key (DEK)
    dek = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)

    # Encrypt the DEK with Google Cloud KMS
    encrypted_dek = client.encrypt(dek)

    return {
        "ciphertext": normalize_base64(ciphertext),
        "encrypted_dek": normalize_base64(encrypted_dek),
        "nonce": normalize_base64(nonce),
        "key_id": os.getenv("GOOGLE_CLOUD_KEY_ID"),
        "algorithm": "AES_256_GCM",
    }


def envelope_decrypt(ciphertext: str, encrypted_dek: str, nonce: str) -> dict:
    client = KMSClient()
    ciphertext_bytes = denormalize_base64(ciphertext)
    encrypted_dek_bytes = denormalize_base64(encrypted_dek)
    nonce_bytes = denormalize_base64(nonce)

    # Decrypt the DEK with Google Cloud KMS
    dek = client.decrypt(encrypted_dek_bytes)
    aesgcm = AESGCM(dek)

    # Decrypt the ciphertext with the DEK
    plaintext_bytes = aesgcm.decrypt(nonce_bytes, ciphertext_bytes, None)

    return {
        "plaintext": plaintext_bytes.decode("utf-8"),
        "key_id": os.getenv("GOOGLE_CLOUD_KEY_ID"),
        "algorithm": "AES_256_GCM",
    }
