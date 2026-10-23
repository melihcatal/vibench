from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError


class SafetyModel:
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.client = boto3.client('bedrock-runtime')

    def request(self, text: str) -> Dict[str, Any]:
        try:
            response = self.client.invoke_model(
                model_id=self.model_id,
                body={
                    'inputText': text
                }
            )
            return response
        except ClientError as e:
            print(f"Error: {e}")
            return {}

    def response(self, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response_body = raw_response.get('body', {})
            return response_body
        except ClientError as e:
            print(f"Error: {e}")
            return {}

    def normalize(self, response_body: Dict[str, Any]) -> Dict[str, Any]:
        try:
            normalized_response = {
                'categories': response_body.get('categories', [])
            }
            return normalized_response
        except ClientError as e:
            print(f"Error: {e}")
            return {}


# Example usage:
# model = SafetyModel('amazon.titan-text-express-v1')
# request_response = model.request('Sample text to moderate')
# normalized_response = model.normalize(model.response(request_response))