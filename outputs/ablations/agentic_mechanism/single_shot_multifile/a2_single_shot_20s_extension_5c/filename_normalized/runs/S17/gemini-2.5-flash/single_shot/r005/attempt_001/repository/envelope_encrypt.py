import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from security_client import SecurityClients
from security_models import (
    EnvelopeEncryptRequest, EnvelopeEncryptResponse,
    EnvelopeDecryptRequest, EnvelopeDecryptResponse
)
from google.cloud import kms_v1

def _local_aes_gcm_encrypt(plaintext: bytes, key: bytes) -> tuple[bytes, bytes, bytes]:
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv, ciphertext, encryptor.tag

def _local_aes_gcm_decrypt(ciphertext: bytes, key: bytes, iv: bytes, tag: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    kms_client = SecurityClients.get_kms_client()

    generate_response = kms_client.generate_data_encryption_key(
        name=request.key_id,
        key_generation_parameters={
            "algorithm": kms_v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm.AES_256
        }
    )
    
    plaintext_dek_bytes = generate_response.plaintext
    encrypted_dek_bytes = generate_response.ciphertext

    plaintext_payload_bytes = request.plaintext.encode("utf-8")
    iv, ciphertext_payload_bytes, tag = _local_aes_gcm_encrypt(plaintext_payload_bytes, plaintext_dek_bytes)

    combined_ciphertext = iv + ciphertext_payload_bytes + tag

    return EnvelopeEncryptResponse(
        encrypted_data_key=base64.b64encode(encrypted_dek_bytes).decode("utf-8"),
        ciphertext=base64.b64encode(combined_ciphertext).decode("utf-8")
    )

def envelope_decrypt(request: EnvelopeDecryptRequest) -> EnvelopeDecryptResponse:
    kms_client = SecurityClients.get_kms_client()

    encrypted_dek_bytes = base64.b64decode(request.encrypted_data_key)
    combined_ciphertext = base64.b64decode(request.ciphertext)

    decrypt_dek_response = kms_client.decrypt(
        name=request.key_id,
        ciphertext=encrypted_dek_bytes
    )
    plaintext_dek_bytes = decrypt_dek_response.plaintext

    iv = combined_ciphertext[:12]
    ciphertext_payload_bytes = combined_ciphertext[12:-16]
    tag = combined_ciphertext[-16:]

    decrypted_payload_bytes = _local_aes_gcm_decrypt(
        ciphertext_payload_bytes, plaintext_dek_bytes, iv, tag
    )

    return EnvelopeDecryptResponse(plaintext=decrypted_payload_bytes.decode("utf-8"))
