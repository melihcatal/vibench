import boto3

BEDROCK_REGION = 'us-east-1'

def get_bedrock_client():
    return boto3.client('bedrock', region_name=BEDROCK_REGION)

def list_foundation_models():
    client = get_bedrock_client()
    response = client.list_foundation_models()
    return response['modelSummaries']

def get_model_details(model_id):
    client = get_bedrock_client()
    response = client.get_foundation_model(modelId=model_id)
    return response['modelDetails']

def invoke_model(model_id, payload):
    client = get_bedrock_client()
    response = client.invoke_model(
        modelId=model_id,
        body=payload
    )
    return response['output']