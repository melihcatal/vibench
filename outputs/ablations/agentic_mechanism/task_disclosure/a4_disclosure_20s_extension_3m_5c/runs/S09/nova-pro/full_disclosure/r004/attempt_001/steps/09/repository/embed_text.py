import boto3

def generate_embedding(text: str) -> dict:
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v1'
    body = {'inputText': text}
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    return response_body

if __name__ == '__main__':
    text = 'Your text string here'
    embedding = generate_embedding(text)
    print(embedding)