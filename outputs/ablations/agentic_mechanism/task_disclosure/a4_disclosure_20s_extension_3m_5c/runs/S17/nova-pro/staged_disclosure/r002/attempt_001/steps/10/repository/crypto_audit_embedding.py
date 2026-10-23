import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_text(text):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

# Example usage
audit_notes = 'Example crypto audit notes.'
embedding = embed_text(audit_notes)
print(embedding)