
class KeyManagementRequest:
    def __init__(self, key_id: str, operation: str, algorithm: str = None, payload: dict = None):
        self.key_id = key_id
        self.operation = operation
        self.algorithm = algorithm
        self.payload = payload

class KeyManagementResponse:
    def __init__(self, key_id: str, status: str, result: dict = None, error: str = None):
        self.key_id = key_id
        self.status = status
        self.result = result
        self.error = error

class EncryptionRequest:
    def __init__(self, key_id: str, data: str, algorithm: str = None):
        self.key_id = key_id
        self.data = data
        self.algorithm = algorithm

class EncryptionResponse:
    def __init__(self, key_id: str, encrypted_data: str = None, decrypted_data: str = None, status: str = None, error: str = None):
        self.key_id = key_id
        self.encrypted_data = encrypted_data
        self.decrypted_data = decrypted_data
        self.status = status
        self.error = error

def normalize_key_management_request(raw_request: dict) -> KeyManagementRequest:
    key_id = raw_request.get("key_id")
    operation = raw_request.get("operation")
    algorithm = raw_request.get("algorithm")
    payload = raw_request.get("payload")
    if not all([key_id, operation]):
        raise ValueError("Missing required fields for KeyManagementRequest")
    return KeyManagementRequest(key_id=key_id, operation=operation, algorithm=algorithm, payload=payload)

def normalize_encryption_request(raw_request: dict) -> EncryptionRequest:
    key_id = raw_request.get("key_id")
    data = raw_request.get("data")
    algorithm = raw_request.get("algorithm")
    if not all([key_id, data]):
        raise ValueError("Missing required fields for EncryptionRequest")
    return EncryptionRequest(key_id=key_id, data=data, algorithm=algorithm)
