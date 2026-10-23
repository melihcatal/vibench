import boto3
from botocore.exceptions import ClientError
import os

class SecurityClient:
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.kms_client = boto3.client("kms", region_name=self.region_name)

    def get_kms_client(self):
        return self.kms_client

    def decrypt_data(self, ciphertext_blob: bytes, key_id: str, encryption_context: dict = None) -> bytes:
        try:
            response = self.kms_client.decrypt(
                CiphertextBlob=ciphertext_blob,
                EncryptionContext=encryption_context or {},
                KeyId=key_id
            )
            return response["Plaintext"]
        except ClientError as e:
            raise RuntimeError(f"AWS KMS Decrypt failed: {e}")

    def encrypt_data_key(self, key_id: str, plaintext: bytes, encryption_context: dict = None) -> dict:
        try:
            response = self.kms_client.encrypt(
                KeyId=key_id,
                Plaintext=plaintext,
                EncryptionContext=encryption_context or {}
            )
            return {
                "CiphertextBlob": response["CiphertextBlob"],
                "KeyId": response["KeyId"]
            }
        except ClientError as e:
            raise RuntimeError(f"AWS KMS Encrypt Data Key failed: {e}")

    def generate_data_key(self, key_id: str, key_spec: str, encryption_context: dict = None) -> dict:
        try:
            response = self.kms_client.generate_data_key(
                KeyId=key_id,
                KeySpec=key_spec,
                EncryptionContext=encryption_context or {}
            )
            return {
                "Plaintext": response["Plaintext"],
                "CiphertextBlob": response["CiphertextBlob"]
            }
        except ClientError as e:
            raise RuntimeError(f"AWS KMS Generate Data Key failed: {e}")

    def sign(self, key_id: str, message: bytes, signing_algorithm: str) -> bytes:
        try:
            response = self.kms_client.sign(
                KeyId=key_id,
                Message=message,
                MessageType='RAW',
                SigningAlgorithm=signing_algorithm
            )
            return response["Signature"]
        except ClientError as e:
            raise RuntimeError(f"AWS KMS Sign failed: {e}")

    def verify(self, key_id: str, message: bytes, signature: bytes, signing_algorithm: str) -> bool:
        try:
            response = self.kms_client.verify(
                KeyId=key_id,
                Message=message,
                MessageType='RAW',
                Signature=signature,
                SigningAlgorithm=signing_algorithm
            )
            return response["SignatureValid"]
        except ClientError as e:
            raise RuntimeError(f"AWS KMS Verify failed: {e}")

