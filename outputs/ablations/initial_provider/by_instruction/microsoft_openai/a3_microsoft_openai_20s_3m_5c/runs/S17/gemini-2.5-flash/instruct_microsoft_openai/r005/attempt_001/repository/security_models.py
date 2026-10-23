from dataclasses import dataclass

@dataclass
class EncryptedPayload:
    ciphertext: str
    key_name: str
    key_vault_url: str
    algorithm: str = 'A256CBC'

@dataclass
class SignedData:
    digest: str
    signature: str
    key_name: str
    key_vault_url: str
    algorithm: str = 'RS256'
