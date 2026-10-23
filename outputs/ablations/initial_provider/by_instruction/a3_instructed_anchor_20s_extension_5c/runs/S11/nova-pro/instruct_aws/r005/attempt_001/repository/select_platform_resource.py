import boto3

def select_model():
    client = boto3.client('bedrock', region_name='us-west-2')
    response = client.list_foundation_models()
    for model in response['modelSummaries']:
        if model['modelId'] == 'amazon.titan-text-express-v1':
            return model['modelId']
    return None