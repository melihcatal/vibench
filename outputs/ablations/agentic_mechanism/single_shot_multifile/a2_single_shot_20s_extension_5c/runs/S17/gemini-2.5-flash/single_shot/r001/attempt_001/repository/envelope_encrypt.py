from security_client import SecurityClients
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse, EnvelopeDecryptionRequest, EnvelopeDecryptionResponse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    kms_client = SecurityClients.get_gcp_kms_client()
    
    # 1. Generate a data encryption key (DEK) from KMS
    # kms_key_id should be in the format: projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING_ID/cryptoKeys/KEY_ID
    crypto_key_name = request.kms_key_id

    generate_key_response = kms_client.generate_data_encryption_key(
        name=crypto_key_name,
        key_length_bytes=32 # AES-256
    )

    plaintext_data_key = generate_key_response.plaintext
    ciphertext_data_key = generate_key_response.ciphertext
    
    # 2. Locally encrypt the payload with the plaintext DEK using AES-256 GCM
    iv = os.urandom(12) # GCM recommended IV size
    cipher = Cipher(algorithms.AES(plaintext_data_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    plaintext_bytes = request.plaintext.encode('utf-8')
    ciphertext_payload = encryptor.update(plaintext_bytes) + encryptor.finalize()
    tag = encryptor.tag

    # Combine IV, ciphertext, and tag for storage
    full_ciphertext_payload = iv + ciphertext_payload + tag

    return EnvelopeEncryptionResponse(
        ciphertext_data_key=ciphertext_data_key,
        ciphertext_payload=full_ciphertext_payload,
        kms_key_id=request.kms_key_id
    )

def envelope_decrypt(request: EnvelopeDecryptionRequest) -> EnvelopeDecryptionResponse:
    kms_client = SecurityClients.get_gcp_kms_client()

    # 1. Decrypt the encrypted data key (DEK) with KMS
    crypto_key_name = request.kms_key_id

    decrypt_key_response = kms_client.decrypt(
        name=crypto_key_name,
        ciphertext=request.ciphertext_data_key
    )
    
    plaintext_data_key = decrypt_key_response.plaintext

    # 2. Locally decrypt the payload with the plaintext DEK
    # Extract IV (12 bytes), ciphertext, and tag (16 bytes)
    iv = request.ciphertext_payload[:12]
    ciphertext_payload_with_tag = request.ciphertext_payload[12:]
    
    ciphertext = ciphertext_payload_with_tag[:-16] 
    tag = ciphertext_payload_with_tag[-16:]

    cipher = Cipher(algorithms.AES(plaintext_data_key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    
    plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()

    return EnvelopeDecryptionResponse(
        plaintext=plaintext_bytes,
        kms_key_id=request.kms_key_id
    )