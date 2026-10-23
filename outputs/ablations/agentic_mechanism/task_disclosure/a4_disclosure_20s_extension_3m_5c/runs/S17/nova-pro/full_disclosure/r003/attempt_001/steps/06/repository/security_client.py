import boto3


class SecurityClient:
    def __init__(self):
        self.kms_client = boto3.client('kms')

    def encrypt(self, plaintext, key_id):
        response = self.kms_client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext
        )
        return response['CiphertextBlob']

    def decrypt(self, ciphertext, key_id):
        response = self.kms_client.decrypt(
            KeyId=key_id,
            CiphertextBlob=ciphertext
        )
        return response['Plaintext']

    def generate_data_key(self, key_id):
        response = self.kms_client.generate_data_key(
            KeyId=key_id,
            KeySpec='AES_256'
        )
        return response['Plaintext'], response['CiphertextBlob']

    def sign(self, message, key_id):
        response = self.kms_client.sign(
            KeyId=key_id,
            Message=message,
            MessageType='RAW'
        )
        return response['Signature']

    def verify(self, message, signature, key_id):
        response = self.kms_client.verify(
            KeyId=key_id,
            Message=message,
            MessageType='RAW',
            Signature=signature
        )
        return response['SignatureValid']