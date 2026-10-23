import boto3

def embed_output(output_text):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': output_text
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__':
    output_text = 'Sample platform output text'
    embedding = embed_output(output_text)
    print(embedding)