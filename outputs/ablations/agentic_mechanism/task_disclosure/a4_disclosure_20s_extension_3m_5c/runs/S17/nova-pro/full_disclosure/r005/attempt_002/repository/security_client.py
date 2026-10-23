from botocore.exceptions import ClientError
import boto3


class SecurityClient:
    def __init__(self, region_name='us-west-2'):
        self.kms_client = boto3.client('kms', region_name=region_name)

    def encrypt(self, plaintext, key_id):
        try:
            response = self.kms_client.encrypt(
                KeyId=key_id,
                Plaintext=plaintext
            )
            return response['CiphertextBlob']
        except ClientError as e:
            print(e)
            return None

    def decrypt(self, ciphertext, key_id):
        try:
            response = self.kms_client.decrypt(
                KeyId=key_id,
                CiphertextBlob=ciphertext
            )
            return response['Plaintext']
        except ClientError as e:
            print(e)
            return None

    def generate_data_key(self, key_id):
        try:
            response = self.kms_client.generate_data_key(
                KeyId=key_id,
                KeySpec='AES_256'
            )
            return response['Plaintext'], response['CiphertextBlob']
        except ClientError as e:
            print(e)
            return None, None

    def sign(self, message, key_id):
        try:
            response = self.kms_client.sign(
                KeyId=key_id,
                Message=message,
                MessageType='RAW'
            )
            return response['Signature']
        except ClientError as e:
            print(e)
            return None

    def verify(self, message, signature, key_id):
        try:
            response = self.kms_client.verify(
                KeyId=key_id,
                Message=message,
                MessageType='RAW',
                Signature=signature
            )
            return response['SignatureValid']
        except ClientError as e:
            print(e)
            return None