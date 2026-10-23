from typing import Any, Dict, List


class EncryptionRequest:
    def __init__(self, plaintext: str, key_id: str):
        self.plaintext = plaintext
        self.key_id = key_id


class EncryptionResponse:
    def __init__(self, ciphertext: str):
        self.ciphertext = ciphertext


class DecryptionRequest:
    def __init__(self, ciphertext: str, key_id: str):
        self.ciphertext = ciphertext
        self.key_id = key_id


class DecryptionResponse:
    def __init__(self, plaintext: str):
        self.plaintext = plaintext


class KeyUsageSummary:
    def __init__(self, key_id: str, usage_count: int, events: List[Dict[str, Any]]):
        self.key_id = key_id
        self.usage_count = usage_count
        self.events = events


def normalize_key_usage(summary: KeyUsageSummary) -> Dict[str, Any]:
    return {
        'key_id': summary.key_id,
        'usage_count': summary.usage_count,
        'events': summary.events
    }