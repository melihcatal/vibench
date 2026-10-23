from security_client import KmsClient
from security_models import EncryptionConfig, Payload, KeyOperationResult

def decrypt_payload(payload: Payload, config: EncryptionConfig) -> KeyOperationResult:
    try:
        kms_client = KmsClient(config)
        decrypted_plaintext = kms_client.decrypt(payload.ciphertext)
        return KeyOperationResult(success=True, data={"plaintext": decrypted_plaintext})
    except Exception as e:
        return KeyOperationResult(success=False, error=str(e))
