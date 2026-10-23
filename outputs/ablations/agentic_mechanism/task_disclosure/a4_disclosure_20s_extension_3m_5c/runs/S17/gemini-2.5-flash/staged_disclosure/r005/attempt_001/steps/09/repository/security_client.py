import os
from cryptography.fernet import Fernet
from google.cloud import kms_v1

class SecurityClient:
    def __init__(self, use_kms: bool = False):
        self.use_kms = use_kms
        if not use_kms:
            self.key = self._get_or_generate_local_key()
            self.f = Fernet(self.key)
        else:
            self.kms_project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
            self.kms_location_id = os.getenv("GOOGLE_CLOUD_KMS_LOCATION", "global")
            self.kms_key_ring_id = os.getenv("GOOGLE_CLOUD_KMS_KEY_RING", "your-key-ring")
            self.kms_key_id = os.getenv("GOOGLE_CLOUD_KMS_KEY", "your-key-name")
            self.kms_client = kms_v1.KeyManagementServiceClient()
            self.kms_key_name = self.kms_client.crypto_key_path(
                self.kms_project_id, self.kms_location_id, self.kms_key_ring_id, self.kms_key_id
            )

    def _get_or_generate_local_key(self):
        key_file = "local_encryption.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
        return key

    def encrypt(self, data: str) -> bytes:
        if self.use_kms:
            # In a real-world scenario, you would use KMS to encrypt data
            # This is a placeholder for KMS encryption.
            # Example:
            # response = self.kms_client.encrypt(request={
            #     "name": self.kms_key_name,
            #     "plaintext": data.encode('utf-8')
            # })
            # return response.ciphertext
            print("Using Google Cloud KMS for encryption (placeholder).")
            return self.f.encrypt(data.encode('utf-8')) # Fallback to local for demonstration
        else:
            return self.f.encrypt(data.encode('utf-8'))

    def decrypt(self, encrypted_data: bytes) -> str:
        if self.use_kms:
            # In a real-world scenario, you would use KMS to decrypt data
            # This is a placeholder for KMS decryption.
            # Example:
            # response = self.kms_client.decrypt(request={
            #     "name": self.kms_key_name,
            #     "ciphertext": encrypted_data
            # })
            # return response.plaintext.decode('utf-8')
            print("Using Google Cloud KMS for decryption (placeholder).")
            return self.f.decrypt(encrypted_data).decode('utf-8') # Fallback to local for demonstration
        else:
            return self.f.decrypt(encrypted_data).decode('utf-8')
