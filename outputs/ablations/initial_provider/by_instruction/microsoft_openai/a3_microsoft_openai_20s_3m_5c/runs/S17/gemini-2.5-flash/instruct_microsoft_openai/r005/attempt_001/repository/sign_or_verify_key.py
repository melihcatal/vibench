from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential
from base64 import b64encode, b64decode
from hashlib import sha256

def sign_payload(key_vault_url: str, key_name: str, payload_digest: bytes) -> str:
    """
    Signs a payload digest using a specified key in Azure Key Vault.
    The payload_digest should be pre-hashed (e.g., with SHA256).
    """
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=key_vault_url, credential=credential)

    # Sign the digest with the specified key. Using RS256 algorithm.
    sign_result = key_client.sign(key_name=key_name, algorithm='RS256', digest=payload_digest)
    
    # The signature is in bytes, convert to base64 string
    signature = b64encode(sign_result.signature).decode('utf-8')
    return signature

def verify_signature(key_vault_url: str, key_name: str, payload_digest: bytes, signature: str) -> bool:
    """
    Verifies a signature against a payload digest using a specified key in Azure Key Vault.
    The payload_digest should be pre-hashed (e.g., with SHA256).
    """
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=key_vault_url, credential=credential)

    # Convert base64 signature to bytes
    signature_bytes = b64decode(signature.encode('utf-8'))

    # Verify the signature with the specified key and algorithm
    verify_result = key_client.verify(key_name=key_name, algorithm='RS256', digest=payload_digest, signature=signature_bytes)
    
    return verify_result.is_valid
