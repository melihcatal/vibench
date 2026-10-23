import boto3

bedrock = boto3.client(service_name='bedrock', region_name='us-east-1')

def embed_text(text):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    embeddings = response['embedding']
    return embeddings