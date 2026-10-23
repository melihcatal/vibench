import boto3

def generate_embedding(text):
    bedrock_client = boto3.client('bedrock', region_name='us-west-2')
    model_id = 'amazon.titan-embed-text-v1'
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body={
            'inputText': text
        }
    )
    embedding = response['embedding']
    return embedding