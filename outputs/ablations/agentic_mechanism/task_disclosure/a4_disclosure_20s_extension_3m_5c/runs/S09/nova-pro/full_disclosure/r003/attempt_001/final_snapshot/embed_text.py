import boto3

def generate_embedding(text: str) -> dict:
    client = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v1'
    body = {'inputText': text}
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    response_body = json.loads(response['body'].read())
    return response_body

if __name__ == '__main__':
    text = 'Sample text for embedding'
    embedding = generate_embedding(text)
    print(embedding)