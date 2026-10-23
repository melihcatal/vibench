import boto3

def embed_output(text):
    bedrock = boto3.client('bedrock')
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    embedding = response['embedding']
    return embedding