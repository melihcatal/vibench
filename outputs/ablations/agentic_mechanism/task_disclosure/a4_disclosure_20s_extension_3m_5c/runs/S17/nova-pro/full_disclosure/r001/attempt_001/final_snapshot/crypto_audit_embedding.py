import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_crypto_audit_notes(notes):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': notes
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']