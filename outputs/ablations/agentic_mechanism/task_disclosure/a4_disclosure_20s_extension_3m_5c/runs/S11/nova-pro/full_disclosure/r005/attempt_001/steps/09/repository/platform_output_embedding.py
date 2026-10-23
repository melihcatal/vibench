import boto3

def embed_output(text):
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')
    model_id = 'amazon.titan-embed-text-v1'
    body = {'inputText': text}
    response = bedrock_client.invoke_model(modelId=model_id, body=body)
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__':
    output_text = 'Sample text to embed'
    embedding = embed_output(output_text)
    print(embedding)