import boto3

def generate_embedding(text):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v1'
    body = {'inputText': text}
    response = bedrock.invoke_model(modelId=model_id, body=body)
    response_body = response['body'].read()
    embedding = json.loads(response_body)['embedding']
    return embedding

if __name__ == '__main__':
    sample_text = 'This is a sample text for embedding.'
    embedding = generate_embedding(sample_text)
    print(embedding)