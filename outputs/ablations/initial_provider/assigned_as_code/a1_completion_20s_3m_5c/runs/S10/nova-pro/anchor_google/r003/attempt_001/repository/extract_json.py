import os

from botocore.exceptions import NoCredentialsError
from boto3 import client


def extract_json(payload, config=None):
    config = config or {}
    prompt = "Extract the following JSON structure from the text:

" + payload["text"] + "

JSON: {""" + payload["json_structure"] + """}"
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
        return {'json': response_body['results'][0]['outputText']}
    except NoCredentialsError:
        return {'error': 'AWS credentials not found'}

