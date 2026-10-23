import boto3

def embed_script(script_text):
    bedrock_client = boto3.client('bedrock-runtime')
    response = bedrock_client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': script_text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__':
    script = 'Your narration script goes here.'
    embedding = embed_script(script)
    print(f'Embedding: {embedding}')
