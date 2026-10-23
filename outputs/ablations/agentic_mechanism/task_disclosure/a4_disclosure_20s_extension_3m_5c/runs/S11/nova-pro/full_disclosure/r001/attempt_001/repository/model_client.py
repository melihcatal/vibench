import os
from botocore.exceptions import NoCredentialsError
import boto3

# Environment variables for AWS credentials
os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'
os.environ['AWS_REGION'] = 'us-west-2'

class ModelClient:
    def __init__(self):
        try:
            self.client = boto3.client('bedrock-runtime')
        except NoCredentialsError:
            raise Exception('AWS credentials not configured')

    def invoke_model(self, model_id, payload):
        response = self.client.invoke_model(
            modelId=model_id,
            body=payload
        )
        return response

# Example usage:
# client = ModelClient()
# response = client.invoke_model('amazon.titan-text-express-v1', {'inputText': 'Hello, world!'})
# print(response)