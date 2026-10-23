import boto3
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Dict, Any

def envelope_encrypt(plaintext: bytes, key_id: str) -> Dict[str, Any]:
    """
    Implements envelope encryption: generate data key from AWS KMS,
    encrypt plaintext with AES-GCM using data key, encrypt data key with KMS.
    """
    client = boto3.client('kms', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    
    # Generate plaintext data key
    gdk_response = client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )
    plaintext_key = gdk_response['PlaintextKey']
    encrypted_key = gdk_response['CiphertextBlob']
    
    # Encrypt payload with AES-GCM
    nonce = os.urandom(12)
    aesgcm = AESGCM(plaintext_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    
    return {
        'ciphertext': ciphertext,
        'nonce': nonce,
        'encrypted_key': encrypted_key
    }
