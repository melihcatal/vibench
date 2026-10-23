import base64
from cryptography.fernet import Fernet
from security_client import SecurityClientConfig
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResult

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResult:
    kms_client = SecurityClientConfig.get_kms_client()
    kms_key_id = request.kms_key_id if request.kms_key_id else SecurityClientConfig.get_kms_encryption_key_id()

    generate_data_key_response = kms_client.generate_data_key(
        KeyId=kms_key_id,
        KeySpec='AES_256'
    )
    
    data_key_plaintext = generate_data_key_response["Plaintext"]
    data_key_ciphertext_blob = generate_data_key_response["CiphertextBlob"]

    fernet_key = base64.urlsafe_b64encode(data_key_plaintext)
    fernet = Fernet(fernet_key)
    
    encrypted_data = fernet.encrypt(request.plaintext_data)

    return EnvelopeEncryptionResult(
        encrypted_data=encrypted_data,
        encrypted_data_key=data_key_ciphertext_blob,
        kms_key_id=kms_key_id
    )