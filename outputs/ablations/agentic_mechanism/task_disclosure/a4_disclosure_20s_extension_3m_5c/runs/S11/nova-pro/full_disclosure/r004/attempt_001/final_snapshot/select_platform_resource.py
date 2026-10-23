import boto3

def select_platform_resource(model_id):
    bedrock_client = boto3.client('bedrock')
    response = bedrock_client.get_model(ModelId=model_id)
    return response
