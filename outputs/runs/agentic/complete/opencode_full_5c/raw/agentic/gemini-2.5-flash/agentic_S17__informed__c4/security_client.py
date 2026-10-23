import os
import base64
from google.cloud import kms_v1
from google.cloud.kms_v1 import types
from google.protobuf import wrappers_pb2

from security_models import (
    EncryptRequest,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
)


class KMSClient:
    def __init__(self):
        self.client = kms_v1.KeyManagementServiceClient()

    def encrypt_payload(self, request: EncryptRequest) -> EncryptResponse:
        aad_bytes = (
            request.additional_authenticated_data
            if request.additional_authenticated_data
            else b""
        )
        ciphertext = self.client.encrypt(
            request.key_id, request.plaintext, additional_authenticated_data=aad_bytes
        ).ciphertext
        return EncryptResponse(ciphertext=ciphertext)

    def decrypt_payload(self, request: DecryptRequest) -> DecryptResponse:
        aad_bytes = (
            request.additional_authenticated_data
            if request.additional_authenticated_data
            else b""
        )
        plaintext = self.client.decrypt(
            request.key_id, request.ciphertext, additional_authenticated_data=aad_bytes
        ).plaintext
        return DecryptResponse(plaintext=plaintext)

    def envelope_encrypt(
        self, request: EnvelopeEncryptRequest
    ) -> EnvelopeEncryptResponse:
        # Generate a new data encryption key (DEK) and encrypt it with the KMS key
        # The `generate_data_encryption_key` method directly returns the encrypted DEK and the plaintext DEK
        # for local encryption.
        aad_bytes = (
            request.additional_authenticated_data
            if request.additional_authenticated_data
            else b""
        )
        generate_dek_response = self.client.generate_data_encryption_key(
            request.key_id,
            types.KeyRing.SymmetricAlgorithm.AES_256,
            additional_authenticated_data=aad_bytes,
        )

        encrypted_dek = generate_dek_response.ciphertext
        plaintext_dek = generate_dek_response.plaintext

        # Locally encrypt the actual payload with the plaintext DEK
        # For simplicity, using a basic XOR encryption here. In a real scenario, use a robust symmetric cipher.
        local_ciphertext = bytes(
            [
                a ^ b
                for a, b in zip(
                    request.plaintext,
                    plaintext_dek * (len(request.plaintext) // len(plaintext_dek) + 1),
                )
            ]
        )

        return EnvelopeEncryptResponse(
            encrypted_data_encryption_key=encrypted_dek, ciphertext=local_ciphertext
        )

    def sign_digest(self, request: SignRequest) -> SignResponse:
        digest_obj = types.Digest()
        # Assume SHA256 for now, as KMS expects a specific digest type
        digest_obj.sha256 = request.digest

        response = self.client.asymmetric_sign(name=request.key_id, digest=digest_obj)
        return SignResponse(signature=response.signature)

    def verify_digest(self, request: VerifyRequest) -> VerifyResponse:
        digest_obj = types.Digest()
        # Assume SHA256 for now
        digest_obj.sha256 = request.digest

        response = self.client.asymmetric_verify(
            name=request.key_id, digest=digest_obj, signature=request.signature
        )
        return VerifyResponse(is_valid=response.verified)
