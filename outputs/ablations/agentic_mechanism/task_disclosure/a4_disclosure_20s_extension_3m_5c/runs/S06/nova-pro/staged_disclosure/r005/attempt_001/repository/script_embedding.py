import boto3

def embed_script(script_text):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': script_text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__':
    script_text = 'Sample narration script for voice-asset search.'
    embedding = embed_script(script_text)
    print(f'Embedding: {embedding}')
