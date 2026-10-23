import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_output(text):
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

if __name__ == '__main__':
    sample_text = 'This is a sample text to be embedded.'
    embedding = embed_output(sample_text)
    print(embedding)