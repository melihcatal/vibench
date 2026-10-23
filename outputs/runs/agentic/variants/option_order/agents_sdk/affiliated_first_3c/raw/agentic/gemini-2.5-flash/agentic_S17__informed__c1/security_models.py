"""
Define local request, response, and normalization helpers for Key Management and Encryption.
For boto3, direct dictionary usage is common, so these are kept minimal.
"""
from typing import Dict, Any, List

class KeyUsageEvent:
    """
    A simple model for a key usage event.
    """
    def __init__(self, event_id: str, event_name: str, event_time: str, key_arn: str, user_identity: Dict[str, Any]):
        self.event_id = event_id
        self.event_name = event_name
        self.event_time = event_time
        self.key_arn = key_arn
        self.user_identity = user_identity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eventId": self.event_id,
            "eventName": self.event_name,
            "eventTime": self.event_time,
            "keyArn": self.key_arn,
            "userIdentity": self.user_identity,
        }

class ModerationResult:
    """
    A simple model for text moderation results.
    """
    def __init__(self, input_text: str, toxicity_score: float, is_unsafe: bool, categories: List[Dict[str, Any]]):
        self.input_text = input_text
        self.toxicity_score = toxicity_score
        self.is_unsafe = is_unsafe
        self.categories = categories

    def to_dict(self) -> Dict[str, Any]:
        return {
            "inputText": self.input_text,
            "toxicityScore": self.toxicity_score,
            "isUnsafe": self.is_unsafe,
            "categories": self.categories,
        }

class AuditNoteEmbedding:
    """
    A simple model for an audit note and its embedding.
    """
    def __init__(self, note_id: str, note_text: str, embedding: List[float]):
        self.note_id = note_id
        self.note_text = note_text
        self.embedding = embedding

    def to_dict(self) -> Dict[str, Any]:
        return {
            "noteId": self.note_id,
            "noteText": self.note_text,
            "embedding": self.embedding,
        }
