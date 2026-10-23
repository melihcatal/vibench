import boto3

def secret_audit_embedding(audit_notes):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': audit_notes
        }
    )
    return response['embedding']