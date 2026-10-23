from typing import Optional, Dict, Any

class SecretMetadata:
    """
    Represents metadata for a secret.
    """
    def __init__(self, name: str, arn: str, description: Optional[str] = None,
                 last_rotated_date: Optional[float] = None,
                 tags: Optional[Dict[str, str]] = None):
        self.name = name
        self.arn = arn
        self.description = description
        self.last_rotated_date = last_rotated_date
        self.tags = tags if tags is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "arn": self.arn,
            "description": self.description,
            "last_rotated_date": self.last_rotated_date,
            "tags": self.tags
        }

class SecretRotationStatus:
    """
    Represents the rotation status of a secret.
    """
    def __init__(self, secret_name: str, enabled: bool, last_rotated_date: Optional[float] = None,
                 rotation_interval_days: Optional[int] = None):
        self.secret_name = secret_name
        self.enabled = enabled
        self.last_rotated_date = last_rotated_date
        self.rotation_interval_days = rotation_interval_days

    def to_dict(self) -> Dict[str, Any]:
        return {
            "secret_name": self.secret_name,
            "enabled": self.enabled,
            "last_rotated_date": self.last_rotated_date,
            "rotation_interval_days": self.rotation_interval_days
        }

