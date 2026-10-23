import boto3

def get_bedrock_client():
    return boto3.client('bedrock-runtime')

def embed_text(text, client):
    response = client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']