import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def embed_log_messages(log_messages):
    bedrock_client = boto3.client('bedrock-runtime')
    embeddings = []
    for message in log_messages:
        try:
            response = bedrock_client.invoke_model(
                model_id='amazon.titan-embed-text-v1',
                body={
                    'inputText': message
                }
            )
            embedding = response['embedding']
            embeddings.append(embedding)
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f'Error embedding message: {e}')
            embeddings.append(None)
    return embeddings

if __name__ == '__main__':
    log_messages = ['Log message 1', 'Log message 2']
    embeddings = embed_log_messages(log_messages)
    print(embeddings)