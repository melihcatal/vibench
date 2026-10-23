import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def embed_text(text):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__':
    document_section = 'Sample text to embed.'
    embedding = embed_text(document_section)
    print(embedding)