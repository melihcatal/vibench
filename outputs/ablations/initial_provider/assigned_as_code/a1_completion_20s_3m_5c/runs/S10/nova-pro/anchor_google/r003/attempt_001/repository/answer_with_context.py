import os

from botocore.exceptions import NoCredentialsError
from boto3 import client


def answer_with_context(payload, config=None):
    config = config or {}
    prompt = "Answer the following question using the provided context:

Question: " + payload["question"] + "

Context: " + payload["context"]
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
        return {'answer': response_body['results'][0]['outputText']}
    except NoCredentialsError:
        return {'error': 'AWS credentials not found'}

