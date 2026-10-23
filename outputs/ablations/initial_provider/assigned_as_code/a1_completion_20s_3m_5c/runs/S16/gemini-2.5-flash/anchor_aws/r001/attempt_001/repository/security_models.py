from typing import Optional, Dict, Any

class SecretPayload:
    secret_id: str
    key_field: Optional[str] = None
    version_id: Optional[str] = None
    version_stage: Optional[str] = None

    def __init__(self, secret_id: str, key_field: Optional[str] = None, version_id: Optional[str] = None, version_stage: Optional[str] = None):
        self.secret_id = secret_id
        self.key_field = key_field
        self.version_id = version_id
        self.version_stage = version_stage

class SecretRotationSummary:
    secret_id: str
    last_rotated_date: Optional[str] = None
    next_rotation_date: Optional[str] = None
    rotation_enabled: bool = False

    def __init__(self, secret_id: str, last_rotated_date: Optional[str] = None, next_rotation_date: Optional[str] = None, rotation_enabled: bool = False):
        self.secret_id = secret_id
        self.last_rotated_date = last_rotated_date
        self.next_rotation_date = next_rotation_date
        self.rotation_enabled = rotation_enabled

class SecretAuditNote:
    secret_id: str
    note_content: str
    embedding: Optional[Any] = None

    def __init__(self, secret_id: str, note_content: str, embedding: Optional[Any] = None):
        self.secret_id = secret_id
        self.note_content = note_content
        self.embedding = embedding

class TranslatedRunbook:
    original_text: str
    translated_text: str
    target_language: str

    def __init__(self, original_text: str, translated_text: str, target_language: str):
        self.original_text = original_text
        self.translated_text = translated_text
        self.target_language = target_language
