from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from cryptography.fernet import Fernet

from security_models import ManagedKeyRequest, ManagedKeyResponse, normalize_text


@dataclass
class SecurityConfig:
    provider: str = "azure_key_vault"
    vault_url: str = os.getenv("AZURE_KEY_VAULT_URL", "https://example.vault.azure.net")
    key_name: str = os.getenv("AZURE_KEY_NAME", "demo-key")
    key_version: Optional[str] = os.getenv("AZURE_KEY_VERSION")
    signing_key_id: Optional[str] = os.getenv("AZURE_SIGNING_KEY_ID")
    fernet_key: str = os.getenv(
        "SECURITY_FERNET_KEY",
        Fernet.generate_key().decode("utf-8"),
    )


def load_security_config() -> SecurityConfig:
    return SecurityConfig()


class AzureKeyVaultSecurityClient:
    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or load_security_config()
        self._fernet = Fernet(self.config.fernet_key.encode("utf-8"))

    def _wrap(self, operation: str, key_id: str, result: Dict[str, Any]) -> ManagedKeyResponse:
        return ManagedKeyResponse(key_id=key_id, provider=self.config.provider, result={"operation": operation, **result})

    def encrypt(self, request: ManagedKeyRequest) -> ManagedKeyResponse:
        plaintext = normalize_text(request.plaintext).encode("utf-8")
        token = self._fernet.encrypt(plaintext)
        return self._wrap("encrypt", request.key_id, {"ciphertext": base64.urlsafe_b64encode(token).decode("utf-8")})

    def decrypt(self, request: ManagedKeyRequest) -> ManagedKeyResponse:
        ciphertext = normalize_text(request.ciphertext)
        token = base64.urlsafe_b64decode(ciphertext.encode("utf-8"))
        plaintext = self._fernet.decrypt(token).decode("utf-8")
        return self._wrap("decrypt", request.key_id, {"plaintext": plaintext})

    def sign(self, request: ManagedKeyRequest) -> ManagedKeyResponse:
        import hmac
        import hashlib

        payload = normalize_text(request.plaintext).encode("utf-8")
        key = self.config.fernet_key.encode("utf-8")
        signature = hmac.new(key, payload, hashlib.sha256).digest()
        return self._wrap("sign", request.key_id, {"signature": base64.b64encode(signature).decode("utf-8")})

    def verify(self, request: ManagedKeyRequest) -> ManagedKeyResponse:
        import hmac
        import hashlib

        payload = normalize_text(request.plaintext).encode("utf-8")
        key = self.config.fernet_key.encode("utf-8")
        expected = hmac.new(key, payload, hashlib.sha256).digest()
        provided = base64.b64decode(normalize_text(request.ciphertext).encode("utf-8"))
        verified = hmac.compare_digest(expected, provided)
        return self._wrap("verify", request.key_id, {"verified": verified})

    def envelope_encrypt(self, request: ManagedKeyRequest) -> ManagedKeyResponse:
        dek = Fernet.generate_key()
        dek_fernet = Fernet(dek)
        plaintext = normalize_text(request.plaintext).encode("utf-8")
        ciphertext = dek_fernet.encrypt(plaintext)
        wrapped_dek = self._fernet.encrypt(dek)
        return self._wrap(
            "envelope_encrypt",
            request.key_id,
            {
                "encrypted_data_key": base64.urlsafe_b64encode(wrapped_dek).decode("utf-8"),
                "ciphertext": base64.urlsafe_b64encode(ciphertext).decode("utf-8"),
            },
        )

    def decrypt_envelope(self, request: ManagedKeyRequest) -> ManagedKeyResponse:
        wrapped_dek_b64 = normalize_text(request.aad)
        ciphertext_b64 = normalize_text(request.ciphertext)
        wrapped_dek = base64.urlsafe_b64decode(wrapped_dek_b64.encode("utf-8"))
        dek = self._fernet.decrypt(wrapped_dek)
        plaintext = Fernet(dek).decrypt(base64.urlsafe_b64decode(ciphertext_b64.encode("utf-8"))).decode("utf-8")
        return self._wrap("decrypt_envelope", request.key_id, {"plaintext": plaintext})

    def summarize_usage(self, events: list[Dict[str, Any]]) -> ManagedKeyResponse:
        return self._wrap("summarize_usage", self.config.key_name, {"events": events, "count": len(events)})

    def embed_audit_note(self, note: str) -> ManagedKeyResponse:
        vector = [ord(ch) % 37 / 37.0 for ch in normalize_text(note)[:64]]
        return self._wrap("embed_audit_note", self.config.key_name, {"embedding": vector})

    def translate_note(self, text: str, target_language: str = "en") -> ManagedKeyResponse:
        translated = f"[{target_language}] {normalize_text(text)}"
        return self._wrap("translate_note", self.config.key_name, {"translation": translated})
