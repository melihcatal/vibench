import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')

def embed_output(output):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': output
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__':
    output = 'Sample platform output for embedding'
    embedding = embed_output(output)
    print(embedding)