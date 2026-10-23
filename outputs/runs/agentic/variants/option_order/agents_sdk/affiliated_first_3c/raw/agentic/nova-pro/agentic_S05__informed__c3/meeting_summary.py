import boto3
from botocore.exceptions import NoCredentialsError

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')

def summarize_meeting(transcript):
    try:
        response = bedrock.invoke_model(
            modelId='amazon.titan-text-express-v1',
            body={
                'inputText': transcript,
                'textGenerationConfig': {
                    'maxTokenCount': 4096,
                    'temperature': 0.5,
                    'topP': 0.9
                }
            }
        )
        return response['body'].read().decode('utf-8')
    except NoCredentialsError:
        print('No AWS credentials found')