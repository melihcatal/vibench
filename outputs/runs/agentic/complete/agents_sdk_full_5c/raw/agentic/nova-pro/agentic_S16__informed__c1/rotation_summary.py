import boto3

def summarize_rotation_status(secret_name):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(ModelId='amazon.titan-embed-text-v1', Body={'inputText': 'Summarize secret rotation status for ' + secret_name})
    return response