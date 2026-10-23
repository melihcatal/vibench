import boto3

def embed_text(text):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__'):
    script = 'Your narration script goes here.'
    embedding = embed_text(script)
    print(f'Embedding: {embedding}')
