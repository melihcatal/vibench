
"""
security_models.py - Define local request, response, and normalization helpers for Key Management and Encryption.
"""

class EncryptRequest:
    def __init__(self, project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes):
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.key_id = key_id
        self.plaintext = plaintext

class EncryptResponse:
    def __init__(self, ciphertext: bytes):
        self.ciphertext = ciphertext

class DecryptRequest:
    def __init__(self, project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes):
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.key_id = key_id
        self.ciphertext = ciphertext

class DecryptResponse:
    def __init__(self, plaintext: bytes):
        self.plaintext = plaintext

class SignRequest:
    def __init__(self, project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, data: bytes):
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.key_id = key_id
        self.version_id = version_id
        self.data = data

class SignResponse:
    def __init__(self, signature: bytes):
        self.signature = signature

class VerifyRequest:
    def __init__(self, project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, data: bytes, signature: bytes):
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.key_id = key_id
        self.version_id = version_id
        self.data = data
        self.signature = signature

class VerifyResponse:
    def __init__(self, is_valid: bool):
        self.is_valid = is_valid

class EnvelopeEncryptRequest:
    def __init__(self, project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext_data: bytes):
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.key_id = key_id
        self.plaintext_data = plaintext_data

class EnvelopeEncryptResponse:
    def __init__(self, encrypted_data: bytes, encrypted_dek: bytes):
        self.encrypted_data = encrypted_data
        self.encrypted_dek = encrypted_dek

class KeyUsageSummaryResponse:
    def __init__(self, total_encrypt_ops: int = 0, total_decrypt_ops: int = 0, total_sign_ops: int = 0):
        self.total_encrypt_ops = total_encrypt_ops
        self.total_decrypt_ops = total_decrypt_ops
        self.total_sign_ops = total_sign_ops

class PayloadSafetyRequest:
    def __init__(self, text_payload: str, project_id: str):
        self.text_payload = text_payload
        self.project_id = project_id

class PayloadSafetyResponse:
    def __init__(self, has_sensitive_data: bool, findings: list):
        self.has_sensitive_data = has_sensitive_data
        self.findings = findings

class CryptoAuditEmbeddingRequest:
    def __init__(self, audit_note: str):
        self.audit_note = audit_note

class CryptoAuditEmbeddingResponse:
    def __init__(self, embedding: list):
        self.embedding = embedding

class ComplianceNoteTranslateRequest:
    def __init__(self, text: str, target_language_code: str, project_id: str):
        self.text = text
        self.target_language_code = target_language_code
        self.project_id = project_id

class ComplianceNoteTranslateResponse:
    def __init__(self, translated_text: str, detected_language_code: str):
        self.translated_text = translated_text
        self.detected_language_code = detected_language_code
