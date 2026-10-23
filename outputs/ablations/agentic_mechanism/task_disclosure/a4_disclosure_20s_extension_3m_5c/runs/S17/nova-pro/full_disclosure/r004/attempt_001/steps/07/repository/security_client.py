import boto3

class SecurityClient:
    def __init__(self, region_name='us-west-2'):
        self.kms_client = boto3.client('kms', region_name=region_name)

    def encrypt(self, plaintext, key_id):
        response = self.kms_client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext
        )
        return response['CiphertextBlob']

    def decrypt(self, ciphertext_blob, key_id):
        response = self.kms_client.decrypt(
            CiphertextBlob=ciphertext_blob,
            KeyId=key_id
        )
        return response['Plaintext']

    def generate_data_key(self, key_id):
        response = self.kms_client.generate_data_key(
            KeyId=key_id,
            KeySpec='AES_256'
        )
        return response['Plaintext'], response['CiphertextBlob']
