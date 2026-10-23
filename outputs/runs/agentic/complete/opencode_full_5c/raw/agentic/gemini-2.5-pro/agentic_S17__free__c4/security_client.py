import os
from google.cloud import kms_v1
from security_models import (
    EncryptRequest,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
)
import hashlib


class SecurityClient:
    def __init__(self):
        self.kms_client = kms_v1.KeyManagementServiceClient()

    def get_key_path(self, key_id, key_ring, location, project_id):
        return self.kms_client.crypto_key_path(project_id, location, key_ring, key_id)

    def encrypt(self, request: EncryptRequest) -> EncryptResponse:
        response = self.kms_client.encrypt(
            request={"name": request.key_path, "plaintext": request.plaintext}
        )
        return EncryptResponse(
            key_path=request.key_path, ciphertext=response.ciphertext
        )

    def decrypt(self, request: DecryptRequest) -> DecryptResponse:
        response = self.kms_client.decrypt(
            request={"name": request.key_path, "ciphertext": request.ciphertext}
        )
        return DecryptResponse(key_path=request.key_path, plaintext=response.plaintext)

    def sign(self, request: SignRequest) -> SignResponse:
        digest = hashlib.sha256(request.message).digest()
        response = self.kms_client.asymmetric_sign(
            request={
                "name": request.key_path,
                "digest": {"sha256": digest},
            }
        )
        return SignResponse(signature=response.signature)

    def verify(self, request: VerifyRequest) -> VerifyResponse:
        digest = hashlib.sha256(request.message).digest()
        response = self.kms_client.asymmetric_decrypt(
            request={"name": request.key_path, "ciphertext": request.signature}
        )
        is_valid = response.plaintext == digest
        return VerifyResponse(is_valid=is_valid)


def get_security_client():
    return SecurityClient()


def get_default_key_path():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("KMS_LOCATION", "global")
    key_ring = os.environ.get("KMS_KEY_RING")
    key_id = os.environ.get("KMS_KEY_ID")

    client = kms_v1.KeyManagementServiceClient()
    return client.crypto_key_path(project_id, location, key_ring, key_id)


def get_default_asymmetric_key_path():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("KMS_LOCATION", "global")
    key_ring = os.environ.get("KMS_KEY_RING")
    key_id = os.environ.get("KMS_ASYMMETRIC_KEY_ID")

    client = kms_v1.KeyManagementServiceClient()
    return client.crypto_key_version_path(project_id, location, key_ring, key_id, "1")
