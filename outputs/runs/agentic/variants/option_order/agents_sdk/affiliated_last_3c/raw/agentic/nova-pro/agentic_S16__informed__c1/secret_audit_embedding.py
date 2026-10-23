import boto3

client = boto3.client('bedrock-runtime')

def secret_audit_embedding(text):
    response = client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    return response['embedding']