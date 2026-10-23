import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_log_messages(log_messages):
    embeddings = []
    for message in log_messages:
        response = bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': message
            }
        )
        embeddings.append(response['embedding'])
    return embeddings