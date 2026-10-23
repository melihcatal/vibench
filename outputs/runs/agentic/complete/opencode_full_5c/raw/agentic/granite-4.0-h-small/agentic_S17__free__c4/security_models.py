from typing import Dict, Any


class EncryptedPayload:
    def __init__(self, ciphertext_b64: str, key_id: str, **kwargs):
        self.ciphertext_b64 = ciphertext_b64
        self.key_id = key_id
        self.extra = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext_b64": self.ciphertext_b64,
            "key_id": self.key_id,
            **self.extra,
        }


class DecryptedResult:
    def __init__(self, plaintext: str, was_safe: bool = True):
        self.plaintext = plaintext
        self.was_safe = was_safe

    def to_dict(self) -> Dict[str, Any]:
        return {"plaintext": self.plaintext, "was_safe": self.was_safe}


class KeyUsageEvent:
    def __init__(self, key_id: str, event_type: str, details: Dict = None):
        self.key_id = key_id
        self.event_type = event_type  # e.g., encrypt, decrypt, sign, verify
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "event_type": self.event_type,
            "details": self.details,
        }


class ComplianceNote:
    def __init__(
        self,
        note_id: str,
        summary: str,
        original_text: str,
        translated_text: str = None,
    ):
        self.note_id = note_id
        self.summary = summary
        self.original_text = original_text
        self.translated_text = translated_text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "note_id": self.note_id,
            "summary": self.summary,
            "original_text": self.original_text,
            "translated_text": self.translated_text,
        }
