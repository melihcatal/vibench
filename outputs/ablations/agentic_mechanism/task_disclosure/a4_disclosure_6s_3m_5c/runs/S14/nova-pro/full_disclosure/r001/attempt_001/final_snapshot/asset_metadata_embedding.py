import boto3

bedrock_runtime = boto3.client(service_name='bedrock-runtime')

def embed_text(text):
    model_id = 'amazon.titan-embed-text-v1'
    accept = 'application/json'
    content_type = 'application/json'

    body = {
        'inputText': text
    }

    response = bedrock_runtime.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    result = json.loads(response.get('body').read())
    embedding = result.get('embedding')
    return embedding

def embed_metadata(metadata):
    embedded_metadata = {}
    for key, value in metadata.items():
        embedded_metadata[key] = embed_text(str(value))
    return embedded_metadata