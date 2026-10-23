import os
import boto3


class KMSClient:
    """Local wrapper around AWS KMS client that provides helper methods."""

    def __init__(self):
        self.client = boto3.client(
            "kms",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def encrypt(self, KeyId: str, Plaintext: bytes):
        return self.client.encrypt(KeyId=KeyId, Plaintext=Plaintext)

    def decrypt(self, CiphertextBlob: bytes):
        return self.client.decrypt(CiphertextBlob=CiphertextBlob)

    def generate_data_key(self, KeyId: str, KeySpec: str):
        return self.client.generate_data_key(KeyId=KeyId, KeySpec=KeySpec)

    def sign(self, KeyId: str, Message: bytes, MessageType: str = "RAW"):
        return self.client.sign(KeyId=KeyId, Message=Message, MessageType=MessageType)

    def verify(
        self, KeyId: str, Message: bytes, Signature: bytes, MessageType: str = "RAW"
    ):
        return self.client.verify(
            KeyId=KeyId, Message=Message, Signature=Signature, MessageType=MessageType
        )


# Singleton instance for reuse across modules
kms_client = KMSClient()
