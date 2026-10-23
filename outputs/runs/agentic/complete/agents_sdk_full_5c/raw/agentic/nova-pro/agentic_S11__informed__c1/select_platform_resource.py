import os
import boto3

bedrock = boto3.client(
    service_name='bedrock',
    region_name='us-east-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

response = bedrock.list_foundation_models()
print(response['modelSummaries'][0]['modelId'])