import boto3

bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def embed_text(text):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    embeddings = response['body'].read()
    return embeddings

# Example usage
audit_note = 'Sample secret audit note'
embeddings = embed_text(audit_note)
print(embeddings)