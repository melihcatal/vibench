import boto3
from botocore.exceptions import NoCredentialsError

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')

def embed_caption(caption):
    try:
        response = bedrock.invoke_model(
            modelId='amazon.titan-embed-text-v1',
            body={
                'inputText': caption
            }
        )
        return response['body'].read().decode('utf-8')
    except NoCredentialsError:
        print('No AWS credentials found')