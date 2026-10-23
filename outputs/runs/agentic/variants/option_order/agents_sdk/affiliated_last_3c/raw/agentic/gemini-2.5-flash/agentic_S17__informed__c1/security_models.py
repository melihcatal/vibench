import json
from typing import Dict, Any, Optional

class EncryptionRequest:
    def __init__(self, plaintext: str, key_id: str):
        if not plaintext or not key_id:
            raise ValueError("Plaintext and Key ID cannot be empty.")
        self.plaintext = plaintext
        self.key_id = key_id

    def to_dict(self) -> Dict[str, Any]:
        return {"plaintext": self.plaintext, "key_id": self.key_id}

class EncryptionResponse:
    def __init__(self, ciphertext_blob: bytes, key_id: str):
        if not ciphertext_blob or not key_id:
            raise ValueError("Ciphertext Blob and Key ID cannot be empty.")
        self.ciphertext_blob = ciphertext_blob
        self.key_id = key_id

    def to_dict(self) -> Dict[str, Any]:
        # For serialization, convert bytes to hex string
        return {"ciphertext_blob_hex": self.ciphertext_blob.hex(), "key_id": self.key_id}

class DecryptionRequest:
    def __init__(self, ciphertext_blob_hex: str, key_id: Optional[str] = None):
        if not ciphertext_blob_hex:
            raise ValueError("Ciphertext Blob (hex) cannot be empty.")
        self.ciphertext_blob = bytes.fromhex(ciphertext_blob_hex)
        self.key_id = key_id # Key ID might not be needed for direct decryption if it's in the blob

    def to_dict(self) -> Dict[str, Any]:
        return {"ciphertext_blob_hex": self.ciphertext_blob.hex(), "key_id": self.key_id}

class DecryptionResponse:
    def __init__(self, plaintext: str, key_id: Optional[str] = None):
        if not plaintext:
            raise ValueError("Plaintext cannot be empty.")
        self.plaintext = plaintext
        self.key_id = key_id

    def to_dict(self) -> Dict[str, Any]:
        return {"plaintext": self.plaintext, "key_id": self.key_id}

class AuditEvent:
    def __init__(self, event_id: str, event_name: str, event_time: str, source_ip_address: str, resources: list):
        self.event_id = event_id
        self.event_name = event_name
        self.event_time = event_time
        self.source_ip_address = source_ip_address
        self.resources = resources

    @classmethod
    def from_cloudtrail_event(cls, cloudtrail_event: Dict[str, Any]):
        event_data = json.loads(cloudtrail_event['message'])
        return cls(
            event_id=event_data.get('eventID', 'N/A'),
            event_name=event_data.get('eventName', 'N/A'),
            event_time=event_data.get('eventTime', 'N/A'),
            source_ip_address=event_data.get('sourceIPAddress', 'N/A'),
            resources=event_data.get('resources', [])
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "event_time": self.event_time,
            "source_ip_address": self.source_ip_address,
            "resources": self.resources
        }
