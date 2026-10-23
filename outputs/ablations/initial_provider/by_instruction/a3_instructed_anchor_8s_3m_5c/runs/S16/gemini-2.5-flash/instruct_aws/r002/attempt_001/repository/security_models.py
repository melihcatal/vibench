from typing import Optional, Dict, Any

class SecretRequest:
    secret_name: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None

    def __init__(self, secret_name: str, version_id: Optional[str] = None, version_stage: Optional[str] = None):
        self.secret_name = secret_name
        self.version_id = version_id
        self.version_stage = version_stage

class SecretResponse:
    secret_string: Optional[str] = None
    secret_binary: Optional[bytes] = None
    response_metadata: Optional[Dict[str, Any]] = None

    def __init__(self, secret_string: Optional[str] = None, secret_binary: Optional[bytes] = None, response_metadata: Optional[Dict[str, Any]] = None):
        self.secret_string = secret_string
        self.secret_binary = secret_binary
        self.response_metadata = response_metadata

class RotationStatus:
    secret_name: str
    rotation_enabled: bool
    last_rotated_date: Optional[float] = None
    next_rotation_date: Optional[float] = None

    def __init__(self, secret_name: str, rotation_enabled: bool, last_rotated_date: Optional[float] = None, next_rotation_date: Optional[float] = None):
        self.secret_name = secret_name
        self.rotation_enabled = rotation_enabled
        self.last_rotated_date = last_rotated_date
        self.next_rotation_date = next_rotation_date

class AuditNote:
    note_id: str
    content: str
    labels: Optional[Dict[str, str]] = None

    def __init__(self, note_id: str, content: str, labels: Optional[Dict[str, str]] = None):
        self.note_id = note_id
        self.content = content
        self.labels = labels
