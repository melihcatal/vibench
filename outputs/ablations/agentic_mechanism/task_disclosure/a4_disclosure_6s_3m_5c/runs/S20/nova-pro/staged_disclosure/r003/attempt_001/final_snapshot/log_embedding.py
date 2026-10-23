import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_log_message(log_message):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': log_message
        }
    )
    embedding = response['embedding']
    return embedding