from typing import Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class EncryptionResult:
    ciphertext: bytes
    key_id: str
    algorithm: str
    iv: Optional[bytes] = None
    additional_authenticated_data: Optional[bytes] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext": base64.b64encode(self.ciphertext).decode("utf-8"),
            "key_id": self.key_id,
            "algorithm": self.algorithm,
            "iv": base64.b64encode(self.iv).decode("utf-8") if self.iv else None,
            "additional_authenticated_data": base64.b64encode(
                self.additional_authenticated_data
            ).decode("utf-8")
            if self.additional_authenticated_data
            else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EncryptionResult":
        return cls(
            ciphertext=base64.b64decode(data["ciphertext"]),
            key_id=data["key_id"],
            algorithm=data["algorithm"],
            iv=base64.b64decode(data["iv"]) if data.get("iv") else None,
            additional_authenticated_data=base64.b64decode(
                data["additional_authenticated_data"]
            )
            if data.get("additional_authenticated_data")
            else None,
        )


@dataclass
class SigningResult:
    signature: bytes
    key_id: str
    algorithm: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature": base64.b64encode(self.signature).decode("utf-8"),
            "key_id": self.key_id,
            "algorithm": self.algorithm,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SigningResult":
        return cls(
            signature=base64.b64decode(data["signature"]),
            key_id=data["key_id"],
            algorithm=data["algorithm"],
        )


@dataclass
class KeyUsageEvent:
    key_id: str
    operation: str
    status: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "operation": self.operation,
            "status": self.status,
            "timestamp": self.timestamp,
            "metadata": self.metadata or {},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KeyUsageEvent":
        return cls(
            key_id=data["key_id"],
            operation=data["operation"],
            status=data["status"],
            timestamp=data["timestamp"],
            metadata=data.get("metadata"),
        )
