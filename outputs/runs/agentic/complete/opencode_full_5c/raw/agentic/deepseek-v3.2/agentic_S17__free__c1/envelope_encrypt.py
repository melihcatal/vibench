import os
import base64
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from google.cloud import kms_v1


def envelope_encrypt(plaintext: str, key_name: str) -> dict:
    """Implement envelope encryption using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()

    # Generate a data encryption key (DEK)
    dek = secrets.token_bytes(32)  # 256-bit key for AES

    # Encrypt the plaintext with the DEK using AES-CBC
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(dek), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plaintext
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()

    # Encrypt
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Encrypt the DEK with KMS (key encryption key)
    dek_encrypt_response = client.encrypt(request={"name": key_name, "plaintext": dek})
    encrypted_dek = dek_encrypt_response.ciphertext

    return {
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "encrypted_dek": base64.b64encode(encrypted_dek).decode("utf-8"),
        "iv": base64.b64encode(iv).decode("utf-8"),
        "key_name": key_name,
        "provider": "google-cloud-kms",
        "algorithm": "AES-256-CBC with KMS-wrapped DEK",
    }


def envelope_decrypt(
    ciphertext_b64: str, encrypted_dek_b64: str, iv_b64: str, key_name: str
) -> dict:
    """Decrypt envelope encrypted data."""
    client = kms_v1.KeyManagementServiceClient()

    # Decode base64 inputs
    ciphertext = base64.b64decode(ciphertext_b64)
    encrypted_dek = base64.b64decode(encrypted_dek_b64)
    iv = base64.b64decode(iv_b64)

    # Decrypt the DEK using KMS
    dek_decrypt_response = client.decrypt(
        request={"name": key_name, "ciphertext": encrypted_dek}
    )
    dek = dek_decrypt_response.plaintext

    # Decrypt the ciphertext with the DEK
    cipher = Cipher(algorithms.AES(dek), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the plaintext
    unpadder = padding.PKCS7(128).unpadder()
    plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()

    plaintext = plaintext_bytes.decode("utf-8")

    return {
        "plaintext": plaintext,
        "key_name": key_name,
        "provider": "google-cloud-kms",
        "algorithm": "AES-256-CBC with KMS-wrapped DEK",
    }


if __name__ == "__main__":
    # Example usage
    key_name = os.environ.get(
        "GCP_KMS_KEY_NAME",
        "projects/my-project/locations/global/keyRings/my-key-ring/cryptoKeys/my-key",
    )
    plaintext = "Sensitive data for envelope encryption"

    encrypted = envelope_encrypt(plaintext, key_name)
    print(f"Envelope encrypted: {encrypted}")

    # To decrypt
    # decrypted = envelope_decrypt(
    #     encrypted['ciphertext'],
    #     encrypted['encrypted_dek'],
    #     encrypted['iv'],
    #     key_name
    # )
    # print(f"Decrypted: {decrypted}")
