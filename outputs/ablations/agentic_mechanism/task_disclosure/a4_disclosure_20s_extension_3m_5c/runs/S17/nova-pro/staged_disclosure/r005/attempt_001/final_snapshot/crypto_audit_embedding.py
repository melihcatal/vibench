import boto3

def embed_notes(notes):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': notes
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__':
    audit_notes = 'Sample crypto audit notes.'
    embedding = embed_notes(audit_notes)
    print(embedding)