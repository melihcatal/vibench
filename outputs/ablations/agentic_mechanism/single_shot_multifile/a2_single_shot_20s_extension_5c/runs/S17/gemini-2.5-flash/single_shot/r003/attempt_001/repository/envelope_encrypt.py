import os
from security_client import get_kms_client, local_aes_gcm_encrypt, local_aes_gcm_decrypt, encode_bytes_to_b64, decode_b64_to_bytes
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse, EnvelopeDecryptionRequest, EnvelopeDecryptionResponse

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    kms_client = get_kms_client()

    generate_key_response = kms_client.generate_data_key(
        KeyId=request.key_id,
        KeySpec='AES_256',
        EncryptionContext=request.encryption_context
    )
    
    plaintext_data_key = generate_key_response['Plaintext']
    encrypted_data_key = generate_key_response['CiphertextBlob']

    ciphertext_bytes, iv_bytes, tag_bytes = local_aes_gcm_encrypt(
        plaintext=request.plaintext.encode('utf-8'),
        key=plaintext_data_key
    )

    return EnvelopeEncryptionResponse(
        encrypted_data_key=encode_bytes_to_b64(encrypted_data_key),
        ciphertext=encode_bytes_to_b64(ciphertext_bytes),
        iv=encode_bytes_to_b64(iv_bytes),
        tag=encode_bytes_to_b64(tag_bytes)
    )

def envelope_decrypt(request: EnvelopeDecryptionRequest) -> EnvelopeDecryptionResponse:
    kms_client = get_kms_client()

    decrypt_key_response = kms_client.decrypt(
        CiphertextBlob=decode_b64_to_bytes(request.encrypted_data_key),
        KeyId=request.key_id,
        EncryptionContext=request.encryption_context
    )
    plaintext_data_key = decrypt_key_response['Plaintext']

    plaintext_bytes = local_aes_gcm_decrypt(
        ciphertext=decode_b64_to_bytes(request.ciphertext),
        key=plaintext_data_key,
        iv=decode_b64_to_bytes(request.iv),
        tag=decode_b64_to_bytes(request.tag)
    )
    
    return EnvelopeDecryptionResponse(
        plaintext=plaintext_bytes.decode('utf-8')
    )
