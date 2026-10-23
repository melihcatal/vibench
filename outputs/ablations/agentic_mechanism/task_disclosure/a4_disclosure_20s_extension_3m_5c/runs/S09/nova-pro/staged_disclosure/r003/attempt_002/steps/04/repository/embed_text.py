import boto3

bedrock = boto3.client('bedrock-runtime')

def generate_embedding(text):
    model_id = 'amazon.titan-embed-text-v1'
    body = {
        'inputText': text
    }
    response = bedrock.invoke_model(
        modelId=model_id,
        body=body
    )
    response_body = json.loads(response['body'].read())
    embedding = response_body['embedding']
    return embedding