from typing import Any, Dict

class SecretModel:
    """Model representing a retrieved secret and related metadata."""
    
    def __init__(self, secret_id: str, version_id: str, payload: Dict[str, Any]):
        self.secret_id = secret_id
        self.version_id = version_id
        self.payload = payload
        self._normalized = self._normalize()
    
    def _normalize(self) -> Dict[str, Any]:
        """Perform common field renaming & type coercion for downstream processing."""
        norm = self.payload.copy()
        if "password" in norm:
            norm["password"] = str(norm["password"]).strip()
        if "created_at" in norm:
            norm["created_at"] = norm["created_at"].isoformat() if hasattr(norm["created_at"], "isoformat") else norm["created_at"]
        return norm
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "version_id": self.version_id,
            "payload": self._normalized,
        }
