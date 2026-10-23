import boto3

def embed_script(script_text):
    bedrock_client = boto3.client('bedrock')
    response = bedrock_client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': script_text
        }
    )
    embeddings = response['embedding']
    return embeddings