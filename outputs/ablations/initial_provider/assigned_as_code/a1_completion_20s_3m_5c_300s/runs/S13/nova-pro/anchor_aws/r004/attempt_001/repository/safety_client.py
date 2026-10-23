import boto3


class ComprehendClient:
    def __init__(self, config):
        self.client = boto3.client('comprehend', region_name=config.get('region', 'us-east-1'))

    def detect_toxic_content(self, text):
        response = self.client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode='en')
        return {'toxicity': response['ResultList'][0]['Toxicity']}