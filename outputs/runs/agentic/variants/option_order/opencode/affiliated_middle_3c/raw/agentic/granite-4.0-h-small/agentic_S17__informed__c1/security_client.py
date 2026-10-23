import os
from google.cloud import kms_v1

# Core utility client wrapping Google Cloud KMS service


class KeyManagementClient:
    _service = "google-cloud-kms"
    _client: kms_v1.KeyManagementServiceClient = None

    def __init__(self, service: str = "/google-cloud-kms"):
        # Instantiate client specific to service (only GCP supported here)
        if service == "google-cloud-kms":
            from google.cloud import kms_v1

            self._client = kms_v1.KeyManagementServiceClient()
        else:
            raise NotImplementedError(f"Service {service} not implemented")

    @property
    def ENVELOPE_SIZE_LIMIT(self) -> int:
        # Google KMS limit for direct encryption (usually 64KB)
        return 63 * 1024

    def _resource_name(self, key_name: str) -> str:
        # Build full resource path for a given key name
        project_id = self._client.project
        location = "global"
        return f"projects/{project_id}/locations/{location}/keyRings/{key_name.split('/')[0]}/cryptoKeys/{key_name.split('/')[-1]}"

    def encrypt(self, plaintext: bytes, key_name: str) -> bytes:
        name = self._resource_name(key_name)
        response = self._client.encrypt(name, plaintext)
        return response.ciphertext

    def decrypt(self, ciphertext: bytes, key_name: str) -> bytes:
        name = self._resource_name(key_name)
        response = self._client.decrypt(name, ciphertext)
        return response.plaintext

    def generate_data_key(self, key_name: str) -> bytes:
        name = self._resource_name(key_name)
        response = self._client.generate_random_bytes(length=32)
        # Actually we generate a new AES key and encrypt it with the given key
        # Leaving simple placeholder: generate random 32‑byte data key
        data_key = response.data
        return data_key

    def encrypt_data_key(self, data_key: bytes, key_name: str) -> bytes:
        name = self._resource_name(key_name)
        encrypt_resp = self._client.encrypt(name, data_key)
        return encrypt_resp.ciphertext

    def decrypt_data_key(self, encrypted_data_key: bytes, key_name: str) -> bytes:
        name = self._resource_name(key_name)
        dec_resp = self._client.decrypt(name, encrypted_data_key)
        return dec_resp.plaintext

    def sign(self, data: bytes, key_name: str) -> bytes:
        name = self._resource_name(key_name)
        sig_resp = self._client.asymmetric_sign(
            name, kms_v1.AsymmetricSignRequest(payload=kms_v1.Digest(sha256=data))
        )
        return sig_resp.signature

    def verify(self, signed_data: bytes, key_name: str) -> bool:
        # For verification we assume caller supplies the signature separately
        # (implementation simplified for demo purpose)
        raise NotImplementedError("Verification not fully implemented in placeholder")


if __name__ == "__main__":
    # Simple sanity check
    key_id = os.getenv("KMS_KEY_ID")
    client = KeyManagementClient()
    print("Client initialized for", client._service)
