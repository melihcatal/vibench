import boto3
from typing import Dict, Any


class SecurityClient:
    def __init__(self, region_name: str):
        self.kms_client = boto3.client("kms", region_name=region_name)
        self.region_name = region_name

    def encrypt(self, key_id: str, plaintext: bytes, encryption_context: Dict[str, str] = None) -> Dict[str, Any]:
        response = self.kms_client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext,
            EncryptionContext=encryption_context or {}
        )
        return response

    def decrypt(self, ciphertext: bytes, encryption_context: Dict[str, str] = None) -> Dict[str, Any]:
        response = self.kms_client.decrypt(
            CiphertextBlob=ciphertext,
            EncryptionContext=encryption_context or {}
        )
        return response

    def generate_data_key(self, key_id: str, key_spec: str = "AES_256", encryption_context: Dict[str, str] = None) -> Dict[str, Any]:
        response = self.kms_client.generate_data_key(
            KeyId=key_id,
            KeySpec=key_spec,
            EncryptionContext=encryption_context or {}
        )
        return response

    def sign(self, key_id: str, message: bytes, signing_algorithm: str, message_type: str = "DIGEST") -> Dict[str, Any]:
        response = self.kms_client.sign(
            KeyId=key_id,
            Message=message,
            SigningAlgorithm=signing_algorithm,
            MessageType=message_type
        )
        return response

    def verify(self, key_id: str, message: bytes, signature: bytes, signing_algorithm: str, message_type: str = "DIGEST") -> Dict[str, Any]:
        response = self.kms_client.verify(
            KeyId=key_id,
            Message=message,
            Signature=signature,
            SigningAlgorithm=signing_algorithm,
            MessageType=message_type
        )
        return response
