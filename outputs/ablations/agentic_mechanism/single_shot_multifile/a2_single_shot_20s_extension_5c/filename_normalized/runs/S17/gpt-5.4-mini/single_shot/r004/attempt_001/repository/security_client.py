from __future__ import annotations

import base64
import hashlib
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import kms_v1
from google.cloud.kms_v1.types import Digest, EncryptRequest, DecryptRequest, AsymmetricSignRequest, AsymmetricVerifyRequest

from security_models import (
    DecryptionRequest,
    DecryptionResult,
    EncryptionRequest,
    EncryptionResult,
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResult,
    SignatureRequest,
    SignatureResult,
    VerificationRequest,
    VerificationResult,
    normalize_ciphertext_bytes,
    normalize_plaintext_bytes,
)


@dataclass
class SecurityClient:
    client: kms_v1.KeyManagementServiceClient
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str

    @property
    def key_name(self) -> str:
        return f"projects/{self.project_id}/locations/{self.location_id}/keyRings/{self.key_ring_id}/cryptoKeys/{self.crypto_key_id}"

    def encrypt(self, request: EncryptionRequest, plaintext_bytes: bytes, aad: bytes | None = None) -> EncryptionResult:
        encrypt_request = EncryptRequest(name=request.key_name, plaintext=plaintext_bytes, additional_authenticated_data=aad or b"")
        response = self.client.encrypt(request=encrypt_request)
        return EncryptionResult(
            ciphertext=base64.b64encode(response.ciphertext).decode("utf-8"),
            plaintext_sha256=hashlib.sha256(plaintext_bytes).hexdigest(),
            metadata={"provider": "google-cloud-kms", "key_version": response.name},
        )

    def decrypt(self, request: DecryptionRequest, ciphertext_bytes: bytes, aad: bytes | None = None) -> DecryptionResult:
        decrypt_request = DecryptRequest(name=request.key_name, ciphertext=normalize_ciphertext_bytes(request.ciphertext), additional_authenticated_data=aad or b"")
        response = self.client.decrypt(request=decrypt_request)
        return DecryptionResult(
            plaintext=response.plaintext.decode("utf-8", errors="replace"),
            metadata={"provider": "google-cloud-kms", "key_version": response.name},
        )

    def envelope_encrypt(self, request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResult:
        dek = os.urandom(32)
        iv = os.urandom(12)
        plaintext_bytes = normalize_plaintext_bytes(request.plaintext)
        encrypted_dek = self.client.encrypt(request=EncryptRequest(name=request.key_name, plaintext=dek)).ciphertext
        ciphertext = base64.b64encode(iv + plaintext_bytes).decode("utf-8")
        return EnvelopeEncryptionResult(
            encrypted_data_key=base64.b64encode(encrypted_dek).decode("utf-8"),
            iv=base64.b64encode(iv).decode("utf-8"),
            ciphertext=ciphertext,
            metadata={"provider": "google-cloud-kms", "algorithm": "envelope"},
        )

    def sign(self, request: SignatureRequest) -> SignatureResult:
        message_bytes = normalize_plaintext_bytes(request.message)
        digest = Digest(sha256=hashlib.sha256(message_bytes).digest())
        sign_request = AsymmetricSignRequest(name=request.key_name, digest=digest)
        response = self.client.asymmetric_sign(request=sign_request)
        return SignatureResult(signature=base64.b64encode(response.signature).decode("utf-8"), metadata={"provider": "google-cloud-kms"})

    def verify(self, request: VerificationRequest) -> VerificationResult:
        message_bytes = normalize_plaintext_bytes(request.message)
        digest = Digest(sha256=hashlib.sha256(message_bytes).digest())
        signature_bytes = base64.b64decode(request.signature.encode("utf-8"))
        verify_request = AsymmetricVerifyRequest(name=request.key_name, digest=digest, signature=signature_bytes)
        response = self.client.asymmetric_verify(request=verify_request)
        return VerificationResult(valid=bool(response.success), metadata={"provider": "google-cloud-kms"})


def get_security_client() -> SecurityClient:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or ""
    location_id = os.environ.get("KMS_LOCATION", "global")
    key_ring_id = os.environ.get("KMS_KEY_RING", "default")
    crypto_key_id = os.environ.get("KMS_KEY_ID", "default")
    client = kms_v1.KeyManagementServiceClient()
    return SecurityClient(client=client, project_id=project_id, location_id=location_id, key_ring_id=key_ring_id, crypto_key_id=crypto_key_id)


def get_kms_key_name(key_name: str | None = None) -> str:
    if key_name:
        return key_name
    security_client = get_security_client()
    return security_client.key_name
