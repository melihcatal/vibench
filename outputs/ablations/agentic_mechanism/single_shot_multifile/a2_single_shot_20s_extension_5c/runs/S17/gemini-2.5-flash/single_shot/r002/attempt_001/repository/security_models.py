from typing import Dict, List, Optional
from datetime import datetime

class EncryptionRequest:
    def __init__(self, plaintext: str, key_id: Optional[str] = None):
        self.plaintext = plaintext
        self.key_id = key_id

class EncryptionResponse:
    def __init__(self, ciphertext_blob: str, key_id: str):
        self.ciphertext_blob = ciphertext_blob
        self.key_id = key_id

class DecryptionRequest:
    def __init__(self, ciphertext_blob: str):
        self.ciphertext_blob = ciphertext_blob

class DecryptionResponse:
    def __init__(self, plaintext: str, key_id: str):
        self.plaintext = plaintext
        self.key_id = key_id

class EnvelopeEncryptionRequest:
    def __init__(self, plaintext: str, key_id: Optional[str] = None):
        self.plaintext = plaintext
        self.key_id = key_id

class EnvelopeEncryptionResponse:
    def __init__(self, ciphertext: str, encrypted_data_key: str, iv: str, kms_key_id: str):
        self.ciphertext = ciphertext
        self.encrypted_data_key = encrypted_data_key
        self.iv = iv
        self.kms_key_id = kms_key_id

class KeyUsageEvent:
    def __init__(self, event_id: str, event_name: str, event_source: str, event_time: datetime, user_identity: Dict, resources: List[Dict]):
        self.event_id = event_id
        self.event_name = event_name
        self.event_source = event_source
        self.event_time = event_time
        self.user_identity = user_identity
        self.resources = resources

class PIIEntity:
    def __init__(self, text: str, type: str, score: float, begin_offset: int, end_offset: int):
        self.text = text
        self.type = type
        self.score = score
        self.begin_offset = begin_offset
        self.end_offset = end_offset

class AuditNote:
    def __init__(self, note_id: str, content: str, timestamp: datetime, metadata: Optional[Dict] = None):
        self.note_id = note_id
        self.content = content
        self.timestamp = timestamp
        self.metadata = metadata if metadata is not None else {}

class TranslatedNote:
    def __init__(self, original_text: str, translated_text: str, source_language: str, target_language: str):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language