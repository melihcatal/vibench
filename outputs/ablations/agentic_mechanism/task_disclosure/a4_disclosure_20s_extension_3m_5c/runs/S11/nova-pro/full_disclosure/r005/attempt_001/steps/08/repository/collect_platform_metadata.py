import boto3

from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class PlatformMetadataCollector:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime')

    def collect_metadata(self, prompt):
        try:
            response = self.bedrock_client.invoke_model(
                model_id='amazon.titan-text-express-v1',
                body={
                    'inputText': prompt,
                    'textGenerationConfig': {
                        'maxTokenCount': 512,
                        'stopSequences': [],
                        'temperature': 0.5,
                        'topP': 0.9
                    }
                }
            )
            model_output = response['body'].read()
            metadata = {
                'usage': response['usage'],
                'model_id': response['model_id'],
                'request_id': response['responseMetadata']['RequestId']
            }
            return model_output, metadata
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f'Error: {e}')
            return None, None
