import boto3

def embed_document_section(section_text):
    client = boto3.client('bedrock-runtime')

    payload = {
        'inputText': section_text,
        'textEmbedding': {
            'modelId': 'amazon.titan-embed-text-v1'
        }
    }

    response = client.invoke_model(
        body=json.dumps(payload),
        modelId='amazon.titan-embed-text-v1'
    )

    result = json.loads(response.get('body').read())
    return result.get('embedding')
