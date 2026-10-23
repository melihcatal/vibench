import boto3

def embed_text(text):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v1'
    body = {'inputText': text}
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding

if __name__ == '__main__':
    platform_output = 'Sample platform output text for embedding.'
    embedding = embed_text(platform_output)
    print(f'Embedding: {embedding}')
