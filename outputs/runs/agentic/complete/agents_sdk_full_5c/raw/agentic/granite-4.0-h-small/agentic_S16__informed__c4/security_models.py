from typing import Dict, Any

class SecretMetadata:
    """Normalized representation of secret metadata."""
    def __init__(self, raw: Dict[str, Any]):
        self.name = raw.get("name")
        self.etag = raw.get("etag")
        self.replication = raw.get("replication")
        self.labels = raw.get("labels", {})
        self.create_time = raw.get("createTime")
        self.update_time = raw.get("updateTime")

    def is_top_secret(self) -> bool:
        """Sample label check for security classification."""
        return self.labels.get("classification", "").lower() == "top-secret"


class RotationPlan:
    """Simple model for a secret rotation policy."""
    def __init__(self, current_version: str, target_version: str, delay_seconds: int = 3600):
        self.current_version = current_version
        self.target_version = target_version
        self.delay_seconds = delay_seconds
        self.status = "pending"  # pending / started / completed

    def start(self) -> None:
        self.status = "started"

    def complete(self) -> None:
        self.status = "completed"
