from typing import Any, Dict

import boto3


class ModelClient:
    def __init__(self, region_name: str, access_key_id: str, secret_access_key: str):
        self.region_name = region_name
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.client = self._create_client()

    def _create_client(self):
        return boto3.client(
            'sagemaker',
            region_name=self.region_name,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key
        )

    def invoke_model(self, model_name: str, payload: Dict[str, Any]):
        response = self.client.invoke_endpoint(
            EndpointName=model_name,
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        return response['Body'].read()

    def get_model_config(self, model_name: str):
        response = self.client.describe_endpoint(
            EndpointName=model_name
        )
        return response['EndpointConfigName']

if __name__ == '__main__':
    client = ModelClient(
        region_name='us-west-2',
        access_key_id='YOUR_AWS_ACCESS_KEY_ID',
        secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY'
    )
    print(client.get_model_config('your-model-name'))