import os
import boto3

def embed_translation(text):
    client = boto3.client('bedrock-runtime', region_name='us-west-2',
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = client.invoke_model(modelId='amazon.titan-embed-text-v1',
                                   body={"inputText": text})
    return response['body']['embedding']

if __name__ == '__main__':
    print(embed_translation('Hello, world!'))