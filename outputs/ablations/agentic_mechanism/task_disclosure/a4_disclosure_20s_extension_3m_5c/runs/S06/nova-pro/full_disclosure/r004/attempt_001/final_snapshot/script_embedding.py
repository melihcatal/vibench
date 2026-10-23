import boto3

def embed_script(script):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v1'
    accept = 'application/json'
    content_type = 'application/json'

    body = {
        'inputText': script
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

if __name__ == '__main__'):
    script = 'This is a sample narration script.'
    embedding = embed_script(script)
    print(embedding)