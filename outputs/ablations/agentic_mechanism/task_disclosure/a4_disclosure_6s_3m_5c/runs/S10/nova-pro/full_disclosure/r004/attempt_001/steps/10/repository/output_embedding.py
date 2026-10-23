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

if __name__ == '__main__':
    sample_text = 'This is a sample text to be embedded.'
    embedding = embed_text(sample_text)
    print(embedding)