import boto3

def invoice_summary(document_path):
    bedrock_client = boto3.client('bedrock-runtime')
    with open(document_path, 'rb') as document:
        response = bedrock_client.invoke_model(ModelId='amazon.titan-text-express-v1', Body=document.read())
    return response