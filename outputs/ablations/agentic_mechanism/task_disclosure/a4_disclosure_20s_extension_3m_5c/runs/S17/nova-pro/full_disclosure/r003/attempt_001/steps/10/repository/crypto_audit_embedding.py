import boto3

def embed_crypto_audit_notes(notes):
    bedrock_client = boto3.client('bedrock')
    response = bedrock_client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': notes
        }
    )
    embeddings = response['embedding']
    return embeddings