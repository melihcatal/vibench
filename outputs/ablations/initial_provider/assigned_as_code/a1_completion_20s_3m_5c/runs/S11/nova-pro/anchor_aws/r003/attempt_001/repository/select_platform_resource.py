import boto3

def select_platform_resource():
    bedrock = boto3.client('bedrock')
    response = bedrock.list_foundation_models()
    model_id = response['modelSummaries'][0]['modelId']
    return model_id