import boto3

def embed_script(script_text):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': script_text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__':
    script = 'This is a sample narration script.'
    embedding = embed_script(script)
    print(embedding)