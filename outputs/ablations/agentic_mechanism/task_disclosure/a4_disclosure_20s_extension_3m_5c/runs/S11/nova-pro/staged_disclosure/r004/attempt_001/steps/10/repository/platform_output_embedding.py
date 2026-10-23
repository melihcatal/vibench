import boto3

def embed_output(text):
    bedrock = boto3.client('bedrock-runtime')
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
    output_text = 'Sample platform output text for embedding.'
    embedding = embed_output(output_text)
    print(embedding)