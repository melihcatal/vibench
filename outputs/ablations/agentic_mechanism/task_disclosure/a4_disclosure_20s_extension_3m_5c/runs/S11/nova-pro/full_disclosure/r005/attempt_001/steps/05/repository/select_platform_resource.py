import os

import boto3

def select_platform_resource(model_id):
    bedrock_client = boto3.client('bedrock', region_name='us-west-2')
    response = bedrock_client.get_foundation_model(modelIdentifier=model_id)
    return response

if __name__ == '__main__':
    model_id = os.getenv('BEDROCK_MODEL_ID')
    if model_id:
        resource = select_platform_resource(model_id)
        print(resource)
    else:
        print('BEDROCK_MODEL_ID environment variable not set.')