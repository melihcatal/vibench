import boto3

def invoke_model():
    bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
    response = bedrock.invoke_model(modelId='amazon.titan-text-express-v1', body=b'{}')
    return response