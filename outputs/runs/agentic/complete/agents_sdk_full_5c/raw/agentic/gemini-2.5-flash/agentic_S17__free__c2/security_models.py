from dataclasses import dataclass

@dataclass
class EnvelopeEncryptionResult:
    encrypted_data: bytes
    encrypted_dek: bytes # Encrypted Data Encryption Key

@dataclass
class KeyUsageEvent:
    timestamp: str
    key_name: str
    operation: str
    user_agent: str
    resource_type: str
    # Add more fields as needed for richer event data

@dataclass
class UnsafeContentDetectionResult:
    has_unsafe_content: bool
    categories: list[str]
    details: str

@dataclass
class CryptoAuditNote:
    id: str
    timestamp: str
    note_text: str
    key_id: str
    operation: str
    # Add more fields relevant for audit

@dataclass
class TranslatedNote:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
