import base64
import os
from dataclasses import dataclass
from typing import Optional, Union

from google.cloud import kms_v1


@dataclass(frozen=True)
class SecurityClientConfig:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    key_version_id: Optional[str] = None

    @classmethod
    def from_env(cls) -> "SecurityClientConfig":
        return cls(
            project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
            location_id=os.environ["GOOGLE_KMS_LOCATION_ID"],
            key_ring_id=os.environ["GOOGLE_KMS_KEY_RING_ID"],
            crypto_key_id=os.environ["GOOGLE_KMS_CRYPTO_KEY_ID"],
            key_version_id=os.getenv("GOOGLE_CLOUD_KMS_KEY_VERSION"),
        )


class SecurityClient:
    def __init__(self, config: Optional[SecurityClientConfig] = None) -> None:
        self.config = config or SecurityClientConfig.from_env()
        self._client = kms_v1.KeyManagementServiceClient()

    def key_name(self) -> str:
        return self._client.crypto_key_path(
            self.config.project_id,
            self.config.location_id,
            self.config.key_ring_id,
            self.config.crypto_key_id,
        )

    def key_version_name(self, key_version_id: Optional[str] = None) -> str:
        version = key_version_id or self.config.key_version_id
        if not version:
            raise ValueError("key version id is required")
        if version.startswith("projects/"):
            return version
        if version.count("/") == 4:
            return version
        return self._client.crypto_key_version_path(
            self.config.project_id,
            self.config.location_id,
            self.config.key_ring_id,
            self.config.crypto_key_id,
            version,
        )

    def encrypt(self, plaintext: Union[str, bytes]) -> str:
        if isinstance(plaintext, str):
            plaintext_bytes = plaintext.encode("utf-8")
        else:
            plaintext_bytes = plaintext
        response = self._client.encrypt(request={"name": self.key_name(), "plaintext": plaintext_bytes})
        return base64.b64encode(response.ciphertext).decode("ascii")

    def decrypt(self, ciphertext: Union[str, bytes]) -> bytes:
        if isinstance(ciphertext, str):
            ciphertext_bytes = base64.b64decode(ciphertext)
        else:
            ciphertext_bytes = ciphertext
        response = self._client.decrypt(request={"name": self.key_name(), "ciphertext": ciphertext_bytes})
        return response.plaintext

    def sign(self, message: Union[str, bytes], key_version_id: Optional[str] = None) -> str:
        if isinstance(message, str):
            message_bytes = message.encode("utf-8")
        else:
            message_bytes = message
        digest = __import__("hashlib").sha256(message_bytes).digest()
        response = self._client.asymmetric_sign(name=self.key_version_name(key_version_id), digest={"sha256": digest})
        return base64.b64encode(response.signature).decode("ascii")

    def verify(self, message: Union[str, bytes], signature_b64: str, key_version_id: Optional[str] = None) -> str:
        if isinstance(message, str):
            message_bytes = message.encode("utf-8")
        else:
            message_bytes = message
        digest = __import__("hashlib").sha256(message_bytes).digest()
        signature = base64.b64decode(signature_b64)
        response = self._client.asymmetric_verify(
            name=self.key_version_name(key_version_id),
            digest={"sha256": digest},
            signature=signature,
        )
        return "verified" if response.success else "failed"


def load_security_client(config: Optional[SecurityClientConfig] = None) -> SecurityClient:
    return SecurityClient(config=config)
