from typing import Dict, Any

class RequestEnvelope:
    """Common request container for KMS operations."""
    def __init__(self, project_id: str, location: str, key_ring: str, crypto_key_id: str, plaintext: Optional[bytes]=None):
        self.project_id = project_id
        self.location = location
        self.key_ring = key_ring
        self.crypto_key_id = crypto_key_id
        self.plaintext = plaintext
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'project_id': self.project_id,
            'location': self.location,
            'key_ring': self.key_ring,
            'crypto_key_id': self.crypto_key_id,
            'plaintext': self.plaintext.decode('utf-8') if self.plaintext else None
        }

class ResponseEnvelope:
    """Unified response wrapper for encryption and signing operations."""
    def __init__(self, ciphertext: Optional[bytes]=None, plaintext: Optional[bytes]=None, wrapped_key: Optional[bytes]=None, nonce: Optional[bytes]=None, signature: Optional[bytes]=None):
        self.ciphertext = ciphertext
        self.plaintext = plaintext
        self.wrapped_key = wrapped_key
        self.nonce = nonce
        self.signature = signature
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'ciphertext': self.ciphertext.decode('base64') if self.ciphertext else None,
            'plaintext': self.plaintext.decode('utf-8') if self.plaintext else None,
            'wrapped_key': self.wrapped_key.decode('base64') if self.wrapped_key else None,
            'nonce': self.nonce.decode('base64') if self.nonce else None,
            'signature': self.signature.decode('base64') if self.signature else None
        }
