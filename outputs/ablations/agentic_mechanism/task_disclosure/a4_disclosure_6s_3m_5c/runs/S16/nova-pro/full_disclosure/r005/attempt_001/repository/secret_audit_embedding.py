import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_secret_audit_notes(notes):
    model_id = 'amazon.titan-embed-text-v1'
    accept = 'application/json'
    content_type = 'application/json'

    body = {
        'inputText': notes
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')

    return embedding