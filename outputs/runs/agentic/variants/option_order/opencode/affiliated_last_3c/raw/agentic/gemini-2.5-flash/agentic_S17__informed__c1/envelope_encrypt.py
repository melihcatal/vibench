from security_client import SecurityClient
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    client = SecurityClient()

    # Generate a data key from KMS
    generate_key_response = client.kms_client.generate_data_key(
        KeyId=request.key_id, KeySpec="AES_256"
    )
    plaintext_data_key = generate_key_response["Plaintext"]
    encrypted_data_key = generate_key_response["CiphertextBlob"]

    # Encrypt the plaintext payload locally using AES-256 GCM
    iv = os.urandom(12)  # 96-bit IV for GCM
    cipher = Cipher(
        algorithms.AES(plaintext_data_key), modes.GCM(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext_blob = (
        encryptor.update(request.plaintext.encode("utf-8")) + encryptor.finalize()
    )
    tag = encryptor.tag

    # Combine IV, ciphertext, and tag
    final_ciphertext = iv + ciphertext_blob + tag

    return EnvelopeEncryptResponse(
        key_id=request.key_id,
        ciphertext_blob=final_ciphertext,
        encrypted_data_key=encrypted_data_key,
    )
