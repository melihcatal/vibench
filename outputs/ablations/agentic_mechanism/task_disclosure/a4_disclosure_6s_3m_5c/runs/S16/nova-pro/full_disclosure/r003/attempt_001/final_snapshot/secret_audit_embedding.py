import boto3

def embed_secret_audit_notes(notes):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': notes
        }
    )
    response_body = json.loads(response.get('body').read())
    return response_body.get('embedding')

if __name__ == '__main__':
    audit_notes = 'Example secret audit notes'
    embedding = embed_secret_audit_notes(audit_notes)
    print(embedding)