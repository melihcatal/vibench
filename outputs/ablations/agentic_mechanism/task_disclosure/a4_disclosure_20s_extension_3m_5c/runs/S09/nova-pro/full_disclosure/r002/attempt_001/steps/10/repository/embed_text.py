import boto3

bedrock = boto3.client('bedrock-runtime')

def generate_embedding(text: str) -> dict:
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
    return {'embedding': embedding}
