import boto3

def generate_embeddings(texts):
    bedrock = boto3.client('bedrock')
    embeddings = []
    for text in texts:
        response = bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': text
            }
        )
        embeddings.append(response['embedding'])
    return embeddings

if __name__ == '__main__'):
    texts = ['Hello, world!', 'This is a test.']
    embeddings = generate_embeddings(texts)
    print(embeddings)