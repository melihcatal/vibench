import boto3

def embed_platform_output(text):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    embedding = response['embedding']
    return embedding