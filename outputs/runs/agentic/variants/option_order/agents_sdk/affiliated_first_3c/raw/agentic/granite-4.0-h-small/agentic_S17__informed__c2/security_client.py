import google.cloud.kms as kms_v1
from google.auth import credentials as gc_credentials

class SecurityClient:
    """Wrapper around provider SDKs for Key Management & Encryption.",
    "Uses Google Cloud KMS (requires GOOGLE_APPLICATION_CREDENTIALS).",
    "Provider identifier appears in the client class import (`kms_v1.KeyManagementServiceClient`)."
    """
    def __init__(self):
        self.client = kms_v1.KeyManagementServiceClient()
        self.project_id = self.client.project_path().split('/')[-1]

    def encrypt(self, plaintext: str, key_name: str) -> str:
        response = self.client.asymmetric_encrypt(name=key_name, plaintext=plaintext.encode('utf-8'))
        return base64.b64encode(response.ciphertext).decode('utf-8')

    def decrypt(self, ciphertext_b64: str, key_name: str) -> str:
        ciphertext = base64.b64decode(ciphertext_b64)
        response = self.client.asymmetric_decrypt(name=key_name, ciphertext=ciphertext)
        return response.plaintext.decode('utf-8')

    def wrap_key(self, plaintext_key: bytes, envelope_key_name: str) -> str:
        wrapped = self.client.asymmetric_encrypt(name=envelope_key_name, plaintext=plaintext_key).ciphertext
        return base64.b64encode(wrapped).decode('utf-8')

    def unwrap_key(self, wrapped_b64: str, envelope_key_name: str) -> bytes:
        wrapped = base64.b64decode(wrapped_b64)
        response = self.client.asymmetric_decrypt(name=envelope_key_name, ciphertext=wrapped)
        return response.plaintext

# Export for other modules
get_kms_client = lambda: SecurityClient().client
# Provider marker: `google.cloud.kms_v1` imports and client class name
