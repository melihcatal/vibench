import os
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError


class AWSKMSClient:
    def __init__(self, key_id: str = None):
        self.key_id = key_id or os.getenv("AWS_KMS_KEY_ID")
        self.client = boto3.client(
            "kms",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def encrypt(self, plaintext: bytes) -> Dict[str, Any]:
        try:
            response = self.client.encrypt(KeyId=self.key_id, Plaintext=plaintext)
            return {
                "ciphertext": response["CiphertextBlob"],
                "key_id": response["KeyId"],
                "algorithm": response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
            }
        except ClientError as e:
            raise Exception(f"AWS KMS encryption failed: {e}")

    def decrypt(self, ciphertext: bytes) -> Dict[str, Any]:
        try:
            response = self.client.decrypt(CiphertextBlob=ciphertext)
            return {
                "plaintext": response["Plaintext"],
                "key_id": response["KeyId"],
                "algorithm": response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
            }
        except ClientError as e:
            raise Exception(f"AWS KMS decryption failed: {e}")

    def generate_data_key(self, key_spec: str = "AES_256") -> Dict[str, Any]:
        try:
            response = self.client.generate_data_key(
                KeyId=self.key_id, KeySpec=key_spec
            )
            return {
                "plaintext_key": response["Plaintext"],
                "ciphertext_key": response["CiphertextBlob"],
                "key_id": response["KeyId"],
            }
        except ClientError as e:
            raise Exception(f"AWS KMS data key generation failed: {e}")

    def sign(
        self, message: bytes, signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"
    ) -> Dict[str, Any]:
        try:
            response = self.client.sign(
                KeyId=self.key_id, Message=message, SigningAlgorithm=signing_algorithm
            )
            return {
                "signature": response["Signature"],
                "key_id": response["KeyId"],
                "signing_algorithm": response["SigningAlgorithm"],
            }
        except ClientError as e:
            raise Exception(f"AWS KMS signing failed: {e}")

    def verify(
        self,
        message: bytes,
        signature: bytes,
        signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    ) -> Dict[str, Any]:
        try:
            response = self.client.verify(
                KeyId=self.key_id,
                Message=message,
                Signature=signature,
                SigningAlgorithm=signing_algorithm,
            )
            return {
                "signature_valid": response["SignatureValid"],
                "key_id": response["KeyId"],
            }
        except ClientError as e:
            raise Exception(f"AWS KMS verification failed: {e}")
