import boto3

bedrock = boto3.client('bedrock-runtime')

def stored_asset_summary(text):
    response = bedrock.invoke_model(modelId='amazon.titan-text-express-v1', body=text)
    return response