import os

import boto3


class SafetyClient:
    def __init__(self):
        self.client = boto3.client('comprehend')

    def detect_toxic_content(self, text):
        response = self.client.detect_toxic_content(
            Text=text,
            LanguageCode='en'
        )
        return response

    def get_configuration(self):
        config = {
            'api_key': os.getenv('AMAZON_COMPREHEND_API_KEY'),
            'region': os.getenv('AMAZON_COMPREHEND_REGION', 'us-west-2')
        }
        return config

if __name__ == '__main__':
    client = SafetyClient()
    print(client.get_configuration())