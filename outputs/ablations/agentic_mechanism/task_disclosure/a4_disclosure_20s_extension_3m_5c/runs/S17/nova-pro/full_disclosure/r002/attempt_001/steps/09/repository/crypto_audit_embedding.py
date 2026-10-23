import boto3

def embed_crypto_audit_notes(notes):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': notes
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']