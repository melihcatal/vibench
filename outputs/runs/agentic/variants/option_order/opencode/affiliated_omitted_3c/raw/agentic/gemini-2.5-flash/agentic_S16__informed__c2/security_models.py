import dataclasses
from typing import List


@dataclasses.dataclass
class SecretRotationSummary:
    secret_name: str
    last_rotated: str
    next_rotation_due: str
    summary_text: str


@dataclasses.dataclass
class SecretLabelSafetyReport:
    secret_name: str
    label: str
    is_safe: bool
    safety_details: str


@dataclasses.dataclass
class AuditNoteEmbedding:
    note_id: str
    embedding: List[float]


@dataclasses.dataclass
class TranslatedRunbook:
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
