import boto3

class SecurityClient:
    def __init__(self, region_name='us-west-2'):
        self.kms_client = boto3.client('kms', region_name=region_name)

    def create_key(self, key_description):
        response = self.kms_client.create_key(Description=key_description)
        return response['KeyMetadata']['KeyId']

    def encrypt(self, key_id, plaintext):
        response = self.kms_client.encrypt(KeyId=key_id, Plaintext=plaintext)
        return response['CiphertextBlob']

    def decrypt(self, ciphertext_blob):
        response = self.kms_client.decrypt(CiphertextBlob=ciphertext_blob)
        return response['Plaintext']
