from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt_payload(
    request: EnvelopeEncryptionRequest,
) -> EnvelopeEncryptionResponse:
    kms_client = get_kms_client()

    data_key_response = kms_client.generate_data_key(
        KeyId=request.key_id, KeySpec="AES_256"
    )

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]

    f = Fernet(Fernet.generate_key(plaintext_data_key))
    encrypted_data = f.encrypt(request.plaintext)

    return EnvelopeEncryptionResponse(
        encrypted_data=encrypted_data, encrypted_data_key=encrypted_data_key
    )
