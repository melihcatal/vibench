import boto3

bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def generate_embedding(text):
    model_id = 'amazon.titan-embed-text-v1'
    body = {
        'inputText': text
    }
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding

# Example usage
audit_note = 'Example crypto audit note'
embedding = generate_embedding(audit_note)
print(embedding)