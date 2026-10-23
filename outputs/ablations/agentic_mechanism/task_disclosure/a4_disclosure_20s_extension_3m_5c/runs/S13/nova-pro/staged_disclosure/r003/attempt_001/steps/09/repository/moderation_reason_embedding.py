import boto3

def generate_embeddings(text):
    bedrock_client = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v1'
    body = {'inputText': text}
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=body
    )
    result = response['body'].read()
    embeddings = result['embedding']
    return embeddings

if __name__ == '__main__':
    rationale = 'Example moderation rationale'
    embeddings = generate_embeddings(rationale)
    print(embeddings)