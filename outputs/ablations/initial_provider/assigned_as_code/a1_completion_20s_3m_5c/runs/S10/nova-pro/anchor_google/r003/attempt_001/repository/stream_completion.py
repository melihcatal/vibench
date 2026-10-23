import os

from botocore.exceptions import NoCredentialsError
from boto3 import client


def stream_completion(payload, config=None):
    config = config or {}
    prompt = payload["text"]
    try:
        bedrock_client = client('bedrock-runtime', region_name=config.get('region') or os.environ['AWS_REGION'])
        response = bedrock_client.invoke_model(
            modelId='amazon.titan-text-express-v1',
            body={
                'inputText': prompt,
                'textGenerationConfig': {
                    'maxTokenCount': 4096,
                    'temperature': 0,
                    'topP': 0.9
                }
            }
        )
        response_body = json.loads(response['body'].read())
        for result in response_body['results']:
            yield result['outputText']
    except NoCredentialsError:
        yield {'error': 'AWS credentials not found'}

