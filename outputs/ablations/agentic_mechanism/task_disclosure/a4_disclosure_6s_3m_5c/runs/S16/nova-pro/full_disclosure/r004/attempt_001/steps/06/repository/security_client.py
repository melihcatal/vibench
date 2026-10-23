import boto3
from botocore.exceptions import ClientError

class SecretManagerClient:
    def __init__(self, region_name='us-west-2'):
        self.client = boto3.client('secretsmanager', region_name=region_name)

    def get_secret(self, secret_name):
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                raise Exception('Decryption failure')
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                raise Exception('Service error')
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                raise Exception('Invalid parameter')
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                raise Exception('Invalid request')
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise Exception('Secret not found')
        else:
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                return secret
            else:
                import base64
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])
                return secret

    def list_secrets(self):
        try:
            response = self.client.list_secrets()
            return response['SecretList']
        except ClientError as e:
            raise Exception('Failed to list secrets') from e

if __name__ == '__main__':
    client = SecretManagerClient()
    secrets = client.list_secrets()
    for secret in secrets:
        print(secret['Name'])