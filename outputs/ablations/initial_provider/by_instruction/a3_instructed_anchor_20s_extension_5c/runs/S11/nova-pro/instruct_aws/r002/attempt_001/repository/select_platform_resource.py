import boto3

def select_resource():
    client = boto3.client('bedrock', region_name='us-west-2')
    model_id = 'anthropic.claude-v2'
    return model_id