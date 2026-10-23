from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptionResponse
import base64
import os
from cryptography.fernet import Fernet


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptionResponse:
    """
    Implements envelope encryption using a managed key service (Google Cloud KMS).
    Generates a data encryption key (DEK) locally, encrypts the plaintext with it,
    then encrypts the DEK with KMS.
    """
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id
    )

    # 1. Generate a data encryption key (DEK) locally
    data_key = Fernet.generate_key()
    f = Fernet(data_key)

    # 2. Encrypt the plaintext with the local DEK
    ciphertext = f.encrypt(request.plaintext.encode("utf-8"))

    # 3. Encrypt the DEK with Google Cloud KMS
    encrypt_dek_response = client.encrypt(
        request={
            "name": key_name,
            "plaintext": data_key,
        }
    )
    encrypted_data_key = encrypt_dek_response.ciphertext

    return EnvelopeEncryptionResponse(
        encrypted_data_key=base64.b64encode(encrypted_data_key).decode("utf-8"),
        ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
    )


if __name__ == "__main__":
    # Example usage:
    project_id = os.environ.get("PROJECT_ID", "your-gcp-project-id")
    location_id = os.environ.get("LOCATION_ID", "global")
    key_ring_id = os.environ.get("KEY_RING_ID", "your-key-ring-id")
    key_id = os.environ.get("KEY_ID", "your-key-id")

    plaintext = "This is a sensitive document for envelope encryption."

    envelope_req = EnvelopeEncryptRequest(
        project_id=project_id,
        location_id=location_id,
        key_ring_id=key_ring_id,
        key_id=key_id,
        plaintext=plaintext,
    )

    try:
        envelope_resp = envelope_encrypt(envelope_req)
        print(f"Encrypted data key (base64): {envelope_resp.encrypted_data_key}")
        print(f"Ciphertext (base64): {envelope_resp.ciphertext}")

        # To demonstrate decryption (not part of the core function, but for testing):
        # In a real scenario, you'd decrypt the encrypted_data_key with KMS first,
        # then use the decrypted data_key to decrypt the ciphertext.
        # This part requires the ability to decrypt the DEK, which would involve another KMS call.

        # For demonstration purposes, assuming we have the original data_key (which we wouldn't in a real scenario without decryption)
        # decrypted_data_key_from_kms = ... # Call KMS to decrypt envelope_resp.encrypted_data_key
        # f_decrypt = Fernet(decrypted_data_key_from_kms)
        # original_plaintext = f_decrypt.decrypt(base64.b64decode(envelope_resp.ciphertext)).decode('utf-8')
        # print(f"Original plaintext after local decryption: {original_plaintext}")

    except Exception as e:
        print(f"Error during envelope encryption: {e}")
