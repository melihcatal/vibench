import json

class SecurityModels:
    """Local data structures for request/response handling.",
    "All fields are provider‑agnostic; concrete serialization is done in security_client.py."
    """
    EncryptRequest = json.loads('''{"plaintext":"str","key_name":"str"}''')
    EncryptResponse = json.loads('''{"ciphertext_b64":"str"}''')
    DecryptRequest = json.loads('''{"ciphertext_b64":"str","key_name":"str"}''')
    DecryptResponse = json.loads('''{"plaintext":"str"}''')

# Simple validation helpers

def validate_encrypt_request(req: dict):
    if not isinstance(req.get('plaintext'), str):
        raise ValueError('plaintext must be a string')
    if not isinstance(req.get('key_name'), str):
        raise ValueError('key_name must be a string')

def validate_decrypt_request(req: dict):
    if not isinstance(req.get('ciphertext_b64'), str):
        raise ValueError('ciphertext_b64 must be a string')
    if not isinstance(req.get('key_name'), str):
        raise ValueError('key_name must be a string')

# Export for reuse
validate_encrypt_request = validate_encrypt_request
validate_decrypt_request = validate_decrypt_request
