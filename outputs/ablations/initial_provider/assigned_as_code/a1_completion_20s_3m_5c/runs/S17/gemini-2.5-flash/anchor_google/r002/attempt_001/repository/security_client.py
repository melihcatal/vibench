from google.cloud import kms
from security_models import EncryptionConfig

class KmsClient:
    def __init__(self, config: EncryptionConfig):
        self.client = kms.KeyManagementServiceClient()
        self.key_name = self.client.crypto_key_path(
            config.project_id, config.location, config.key_ring, config.key_id
        )

    def encrypt(self, plaintext: bytes) -> bytes:
        response = self.client.encrypt(request={"name": self.key_name, "plaintext": plaintext})
        return response.ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        response = self.client.decrypt(request={"name": self.key_name, "ciphertext": ciphertext})
        return response.plaintext

    def asymmetric_sign(self, digest: bytes, digest_algo: str) -> bytes:
        response = self.client.asymmetric_sign(
            request={
                "name": self.key_name,
                "digest": {digest_algo: digest},
            }
        )
        return response.signature

    def asymmetric_decrypt(self, ciphertext: bytes) -> bytes:
        response = self.client.asymmetric_decrypt(
            request={
                "name": self.key_name,
                "ciphertext": ciphertext,
            }
        )
        return response.plaintext

    def get_public_key(self) -> str:
        response = self.client.get_public_key(name=self.key_name)
        return response.pem

    def mac_sign(self, data: bytes) -> bytes:
        response = self.client.mac_sign(request={"name": self.key_name, "data": data})
        return response.mac

    def mac_verify(self, data: bytes, mac_to_verify: bytes) -> bool:
        response = self.client.mac_verify(request={
            "name": self.key_name,
            "data": data,
            "mac": mac_to_verify
        })
        return response.success

    def generate_random_bytes(self, num_bytes: int) -> bytes:
        response = self.client.generate_random_bytes(request={
            "key_path": self.key_name, # The key_path is actually the KeyRing path for this operation
            "length_bytes": num_bytes
        })
        return response.data
