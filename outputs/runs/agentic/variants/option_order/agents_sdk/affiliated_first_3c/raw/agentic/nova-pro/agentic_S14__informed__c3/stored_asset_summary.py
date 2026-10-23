import boto3

def stored_asset_summary(text):
    bedrock_client = boto3.client('bedrock-runtime')
    response = bedrock_client.invoke_model(ModelId='amazon.titan-text-express-v1', Body=text)
    return response