import boto3

bedrock_client = boto3.client('bedrock-runtime')

def generate_embedding(text):
    response = bedrock_client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    embedding = response['embedding']
    return embedding