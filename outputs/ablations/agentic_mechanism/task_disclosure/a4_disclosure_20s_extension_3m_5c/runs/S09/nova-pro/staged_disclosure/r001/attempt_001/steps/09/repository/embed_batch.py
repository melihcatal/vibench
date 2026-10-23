import boto3

def generate_embeddings(texts):
    bedrock = boto3.client('bedrock-runtime')
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
    texts = ['sample text 1', 'sample text 2']
    embeddings = generate_embeddings(texts)
    print(embeddings)