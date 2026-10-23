from security_client import KmsClient
from security_models import EncryptionConfig, Payload, KeyOperationResult
from cryptography.fernet import Fernet

def envelope_encrypt(payload: Payload, config: EncryptionConfig) -> KeyOperationResult:
    try:
        kms_client = KmsClient(config)

        # Generate a data encryption key (DEK) locally
        data_key = Fernet.generate_key()
        f = Fernet(data_key)

        # Encrypt the actual payload with the local DEK
        encrypted_data = f.encrypt(payload.plaintext)

        # Encrypt the DEK with KMS
        encrypted_data_key = kms_client.encrypt(data_key)

        return KeyOperationResult(
            success=True,
            data={
                "encrypted_data": encrypted_data,
                "encrypted_data_key": encrypted_data_key,
            },
        )
    except Exception as e:
        return KeyOperationResult(success=False, error=str(e))

def envelope_decrypt(encrypted_data: bytes, encrypted_data_key: bytes, config: EncryptionConfig) -> KeyOperationResult:
    try:
        kms_client = KmsClient(config)

        # Decrypt the DEK with KMS
        decrypted_data_key = kms_client.decrypt(encrypted_data_key)

        # Decrypt the actual payload with the decrypted DEK
        f = Fernet(decrypted_data_key)
        decrypted_payload = f.decrypt(encrypted_data)

        return KeyOperationResult(success=True, data={"plaintext": decrypted_payload})
    except Exception as e:
        return KeyOperationResult(success=False, error=str(e))
