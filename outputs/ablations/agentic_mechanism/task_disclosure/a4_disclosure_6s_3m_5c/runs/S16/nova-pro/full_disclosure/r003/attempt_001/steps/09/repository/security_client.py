import boto3

class SecretManagementClient:
    def __init__(self, region_name='us-west-2'):
        self.client = boto3.client('secretsmanager', region_name=region_name)

    def get_secret_value(self, secret_name):
        response = self.client.get_secret_value(SecretId=secret_name)
        return response['SecretString']

    def list_secrets(self):
        response = self.client.list_secrets()
        return response['SecretList']