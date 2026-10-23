import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def generate_embedding(text):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    result = response['body'].read()
    embedding = result['embedding']
    return embedding

if __name__ == '__main__':
    text = 'Your text string here'
    embedding = generate_embedding(text)
    print(embedding)