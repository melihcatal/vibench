import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def embed_text(text):
    model_id = 'amazon.titan-embed-text-v1'
    accept = 'application/json'
    content_type = 'application/json'

    body = {
        'inputText': text
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    response_body = json.loads(response.get('body').read())
    embeddings = response_body.get('embedding')

    return embeddings

# Example usage
audit_notes = 'Example crypto audit note'
embeddings = embed_text(audit_notes)
print(embeddings)