import boto3

bedrock = boto3.client('bedrock-runtime')

def asset_metadata_embedding(text):
    response = bedrock.invoke_model(modelId='amazon.titan-embed-text-v1', body=text)
    return response