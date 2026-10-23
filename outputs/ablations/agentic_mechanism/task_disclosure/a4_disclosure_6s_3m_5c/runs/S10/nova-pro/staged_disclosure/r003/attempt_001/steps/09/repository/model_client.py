import boto3

BEDROCK_REGION = 'us-west-2'

def create_bedrock_client():
    return boto3.client('bedrock-runtime', region_name=BEDROCK_REGION)

def select_model_family(model_family):
    model_ids = {
        'amazon-nova-api/nova-pro-v1': 'amazon.nova-pro-v1',
        'amazon-titan-text-express-v1': 'amazon.titan-text-express-v1',
        'amazon-titan-text-lite-v1': 'amazon.titan-text-lite-v1'
    }
    return model_ids.get(model_family, 'amazon.nova-pro-v1')

def invoke_model(client, model_id, payload):
    response = client.invoke_model(
        modelId=model_id,
        body=payload
    )
    return response['body'].read().decode('utf-8')