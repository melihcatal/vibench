import json

def normalize_payload(data):
    # Basic normalization for consistency
    if isinstance(data, dict):
        return json.dumps(data, sort_keys=True).encode('utf-8')
    elif isinstance(data, str):
        return data.encode('utf-8')
    elif isinstance(data, bytes):
        return data
    else:
        raise TypeError("Unsupported payload type for normalization.")

def denormalize_response(data):
    # Basic denormalization for consistency
    if isinstance(data, bytes):
        try:
            return json.loads(data.decode('utf-8'))
        except json.JSONDecodeError:
            return data.decode('utf-8')
    return data

# Example request/response structures (can be expanded as needed)
class EncryptionRequest:
    def __init__(self, plaintext: bytes, key_id: str = None):
        self.plaintext = plaintext
        self.key_id = key_id

class EncryptionResponse:
    def __init__(self, ciphertext: bytes, iv: bytes, tag: bytes, key_id: str, algorithm: str):
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.key_id = key_id
        self.algorithm = algorithm

class DecryptionRequest:
    def __init__(self, ciphertext: bytes, iv: bytes, tag: bytes, key_id: str):
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.key_id = key_id

class DecryptionResponse:
    def __init__(self, plaintext: bytes):
        self.plaintext = plaintext
