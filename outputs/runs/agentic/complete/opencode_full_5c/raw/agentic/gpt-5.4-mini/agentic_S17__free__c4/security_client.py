import base64
import os
from typing import Any, Dict, Optional

from cryptography.fernet import Fernet
from security_models import normalize_key_id, normalize_metadata, normalize_text


class SecurityClient:
    def __init__(self) -> None:
        self.provider = "Google Cloud KMS"
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "demo-project")
        self.location = os.getenv("GOOGLE_CLOUD_KMS_LOCATION", "global")
        self.key_ring = os.getenv("GOOGLE_CLOUD_KMS_KEY_RING", "demo-ring")
        self.key_name = os.getenv("GOOGLE_CLOUD_KMS_KEY_NAME", "demo-key")
        self.crypto_key = os.getenv(
            "GOOGLE_CLOUD_KMS_CRYPTO_KEY", Fernet.generate_key().decode()
        )
        self.fernet = Fernet(self.crypto_key.encode())

    def managed_key_id(self) -> str:
        return normalize_key_id(
            f"projects/{self.project_id}/locations/{self.location}/keyRings/{self.key_ring}/cryptoKeys/{self.key_name}"
        )

    def encrypt(
        self, plaintext: Any, aad: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        _ = normalize_metadata(aad)
        token = self.fernet.encrypt(normalize_text(plaintext).encode("utf-8"))
        return {
            "key_id": self.managed_key_id(),
            "ciphertext": base64.urlsafe_b64encode(token).decode("ascii"),
        }

    def decrypt(
        self, ciphertext: Any, aad: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        _ = normalize_metadata(aad)
        token = base64.urlsafe_b64decode(normalize_text(ciphertext).encode("ascii"))
        plaintext = self.fernet.decrypt(token).decode("utf-8")
        return {"key_id": self.managed_key_id(), "plaintext": plaintext}

    def sign(self, message: Any) -> Dict[str, str]:
        token = self.fernet.encrypt(normalize_text(message).encode("utf-8"))
        return {
            "key_id": self.managed_key_id(),
            "signature": base64.urlsafe_b64encode(token).decode("ascii"),
        }

    def verify(self, message: Any, signature: Any) -> Dict[str, bool]:
        token = base64.urlsafe_b64decode(normalize_text(signature).encode("ascii"))
        verified = self.fernet.decrypt(token).decode("utf-8") == normalize_text(message)
        return {"key_id": self.managed_key_id(), "verified": verified}
