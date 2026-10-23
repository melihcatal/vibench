import boto3

bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

def embed_script(script_text):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': script_text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__'):
    script = 'Your narration script goes here.'
    embedding = embed_script(script)
    print(f'Embedding: {embedding}')
