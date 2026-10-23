
class KeyManagementRequest:
    def __init__(self, key_id: str, payload: bytes):
        self.key_id = key_id
        self.payload = payload

class KeyManagementResponse:
    def __init__(self, key_id: str, encrypted_payload: bytes, iv: bytes):
        self.key_id = key_id
        self.encrypted_payload = encrypted_payload
        self.iv = iv

class EncryptionRequest:
    def __init__(self, data: bytes, encryption_key: bytes):
        self.data = data
        self.encryption_key = encryption_key

class EncryptionResponse:
    def __init__(self, encrypted_data: bytes, iv: bytes):
        self.encrypted_data = encrypted_data
        self.iv = iv

def normalize_payload(data: dict) -> bytes:
    """Normalizes a dictionary payload into bytes for consistent encryption/decryption."""
    import json
    return json.dumps(data, sort_keys=True).encode('utf-8')

def denormalize_payload(data: bytes) -> dict:
    """Denormalizes bytes into a dictionary payload after decryption."""
    import json
    return json.loads(data.decode('utf-8'))
