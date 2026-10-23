import boto3

bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def generate_embedding(text):
    model_id = 'amazon.titan-embed-text-v1'
    body = {'inputText': text}
    response = bedrock.invoke_model(modelId=model_id, body=body)
    response_body = response['body'].read()
    embedding = response_body['embedding']
    return embedding

if __name__ == '__main__':
    text = 'This is a sample text to generate an embedding vector.'
    embedding = generate_embedding(text)
    print(embedding)