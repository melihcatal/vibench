from security_client import KmsClient
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse
import os


# A simple XOR-based local encryption for demonstration purposes.
# This is NOT production-grade encryption.
def xor_encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ k for d, k in zip(data, key * (len(data) // len(key) + 1)))


def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    kms_client = KmsClient().get_client()

    # 1. Generate a data key from KMS
    generate_data_key_response = kms_client.generate_data_key(
        KeyId=request.key_id,
        KeySpec="AES_256",
        EncryptionContext=request.encryption_context,
    )

    plaintext_data_key = generate_data_key_response["Plaintext"]
    encrypted_data_key = generate_data_key_response["CiphertextBlob"]

    # 2. Locally encrypt the payload using the plaintext data key
    ciphertext_payload = xor_encrypt_decrypt(
        request.plaintext.encode("utf-8"), plaintext_data_key
    )

    # 3. Return the encrypted data key and the locally encrypted payload
    return EnvelopeEncryptionResponse(
        encrypted_data_key=encrypted_data_key,
        ciphertext_payload=ciphertext_payload,
        key_id=request.key_id,
        encryption_context=request.encryption_context,
    )
