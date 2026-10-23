import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

bedrock = boto3.client('bedrock-runtime')

def embed_caption(caption):
    try:
        response = bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': caption
            }
        )
        response_body = json.loads(response['body'].read())
        return response_body['embedding']
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'Error: {e}')
        return None

if __name__ == '__main__':
    sample_caption = 'This is a sample caption for a meeting.'
    embedding = embed_caption(sample_caption)
    if embedding:
        print(f'Embedding: {embedding}')
    else:
        print('Failed to generate embedding.')