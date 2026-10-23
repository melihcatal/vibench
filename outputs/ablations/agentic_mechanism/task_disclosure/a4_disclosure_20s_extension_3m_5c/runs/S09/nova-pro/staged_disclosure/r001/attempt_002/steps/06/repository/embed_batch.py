import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def generate_embeddings(texts):
    embeddings = []
    for text in texts:
        response = bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': text
            }
        )
        embedding = response['embedding']
        embeddings.append(embedding)
    return embeddings

if __name__ == '__main__':
    texts = ['sample text 1', 'sample text 2']
    embeddings = generate_embeddings(texts)
    print(embeddings)